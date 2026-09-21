"""End-to-end solver behaviour: notebook equivalence, analytic optimum, independent cross-check."""
import json
import os

import numpy as np
import pytest

from tvinpaint import operators
from tvinpaint.operators import divergence, gradient, tv_energy
from tvinpaint.solver import pdr_inpaint

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _notebook_namespace(f, known):
    """Execute the notebook's own function cells verbatim on a small problem."""
    nb = json.load(open(os.path.join(REPO, "Adebanji_Image_Inpainting.ipynb")))
    ns = {"np": np, "xdim": f.shape[0], "ydim": f.shape[1], "newimagedata": f.copy(),
          "newlossdata": np.where(known, 0.0, 255.0)}
    wanted = ["def gradient", "def divergence", "mask_red = np.zeros", "def neighbor_sum",
              "alpha = 1.0", "def sym_red_black_gauss_seidel", "def tv_inpainting"]
    seen = set()
    for c in nb["cells"]:
        src = "".join(c["source"])
        if c["cell_type"] != "code":
            continue
        for w in wanted:
            if w in src and w not in seen:
                exec(src, ns)
                seen.add(w)
                break
    assert seen == set(wanted)
    return ns


def _problem(seed=0, shape=(28, 33)):
    rng = np.random.default_rng(seed)
    f = np.round(255 * rng.random(shape))
    known = np.ones(shape, dtype=bool)
    known[8:16, 10:20] = False
    known[3, :] = False
    f[~known] = 255.0
    return f, known


def test_legacy_mode_is_bitwise_identical_to_the_notebook():
    f, known = _problem()
    ns = _notebook_namespace(f, known)
    p0 = np.zeros((2,) + f.shape)
    u, p, u_bar, p_bar = ns["tv_inpainting"](25, 3, 14, 1 / 14, f.copy(), p0, f.copy(), p0.copy())
    r = pdr_inpaint(f, known, iters=25, n_sweeps=3, sigma=14, legacy=True)
    assert np.array_equal(r.u_dr, u) and np.array_equal(r.p, p)
    assert np.array_equal(r.u_bar, u_bar) and np.array_equal(r.p_bar, p_bar)


def test_legacy_flag_cannot_be_mixed_with_the_ablation_switches():
    f, known = _problem()
    with pytest.raises(ValueError):
        pdr_inpaint(f, known, iters=1, legacy=True, sweep="symmetric")
    with pytest.raises(ValueError):
        pdr_inpaint(f, known, iters=1, legacy=True, mu_weighted=True)


def test_defaults_are_the_verified_variant():
    f, known = _problem(6)
    a = pdr_inpaint(f, known, iters=20)
    b = pdr_inpaint(f, known, iters=20, sweep="symmetric", mu_weighted=True)
    assert np.array_equal(a.u, b.u) and np.array_equal(a.u_dr, b.u_dr)
    assert not np.array_equal(a.u_dr, pdr_inpaint(f, known, iters=20, legacy=True).u_dr)


def test_deterministic():
    f, known = _problem(1)
    a = pdr_inpaint(f, known, iters=30).u
    b = pdr_inpaint(f, known, iters=30).u
    assert np.array_equal(a, b)


@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize("iters", [1, 40, 400])
def test_returned_solution_satisfies_the_hard_constraint_exactly(legacy, iters):
    """The authoritative result `.u` equals f on the known pixels bit for bit (not just to a
    tolerance), whatever the iteration count or mode."""
    f, known = _problem(2)
    r = pdr_inpaint(f, known, iters=iters, legacy=legacy)
    assert np.array_equal(r.u[known], f[known])
    assert np.abs(r.u[known] - f[known]).max() == 0.0


def test_raw_douglas_rachford_iterate_is_not_feasible_at_finite_iterations():
    """Why the raw iterate is not returned: it violates the constraint, the feasible one does not."""
    f, known = _problem(2)
    r = pdr_inpaint(f, known, iters=40, legacy=True)
    assert np.abs(r.u_dr[known] - f[known]).max() > 1e-3
    assert np.abs(r.u[known] - f[known]).max() == 0.0


def test_feasible_and_raw_iterates_converge_to_the_same_limit():
    f, known, _ = _strip_problem()
    r = pdr_inpaint(f, known, iters=1500)
    assert np.abs(r.u - r.u_dr).max() < 1e-3


def _strip_problem(rows=12, cols=20, left=6, right=6, a=10.0, b=90.0):
    f = np.zeros((rows, cols))
    known = np.zeros((rows, cols), dtype=bool)
    f[:, :left], f[:, cols - right:] = a, b
    known[:, :left] = True
    known[:, cols - right:] = True
    f[~known] = 255.0
    return f, known, rows * abs(b - a)


@pytest.mark.parametrize("sweep", ["forward", "symmetric"])
def test_analytic_optimum_two_constant_columns(sweep):
    """Every row must climb from a to b, so TV >= rows*|b-a| for any feasible image, with
    equality for a monotone interpolation. The feasible iterate must approach this exact value."""
    f, known, lower = _strip_problem()
    r = pdr_inpaint(f, known, iters=1500, sweep=sweep)
    e = tv_energy(r.u)
    assert e >= lower - 1e-9                     # rigorous lower bound for a feasible image
    assert e == pytest.approx(lower, rel=2e-3)


def test_constant_data_gives_constant_image():
    f = np.full((20, 22), 42.0)
    known = np.ones_like(f, dtype=bool)
    known[5:12, 6:15] = False
    f[~known] = 255.0
    r = pdr_inpaint(f, known, iters=600)
    assert np.abs(r.u - 42.0).max() < 0.5
    assert tv_energy(r.u) < 0.02 * tv_energy(f)


def _pdhg_tv_inpaint(f, known, iters=20000):
    """Independent solver (Chambolle-Pock) for the same hard-constrained problem."""
    tau = sig = 0.35                             # sig*tau*||K||^2 <= 0.98 < 1
    u = f.copy()
    ub = u.copy()
    p = np.zeros((2,) + f.shape)
    for _ in range(iters):
        p = p + sig * gradient(ub)
        p = p / np.maximum(np.sqrt((p ** 2).sum(0)), 1)
        un = u + tau * divergence(p)             # u - tau*K^T p, with K^T = -div
        un[known] = f[known]
        ub = 2 * un - u
        u = un
    return u


def test_agrees_with_an_independent_solver_on_energy():
    """The minimiser need not be unique, so compare the optimal energy, not pixels."""
    rng = np.random.default_rng(3)
    f = np.zeros((26, 30))
    f[:, 15:] = 60.0
    f[10:20, 5:12] += 40.0
    f += np.round(rng.random(f.shape) * 3)
    known = np.ones_like(f, dtype=bool)
    known[8:18, 9:21] = False
    f[~known] = 255.0
    e_pdr = tv_energy(pdr_inpaint(f, known, iters=3000).u)
    e_cp = tv_energy(_pdhg_tv_inpaint(f, known))
    assert e_pdr == pytest.approx(e_cp, rel=3e-3)


def test_energy_of_feasible_iterate_decreases_toward_the_optimum():
    f, known, lower = _strip_problem()
    hist = []
    pdr_inpaint(f, known, iters=400,
                callback=lambda k, u, ut, p: hist.append(tv_energy(ut)))
    assert hist[0] > 2 * lower                    # the white hole starts far above the optimum
    assert hist[-1] < 1.02 * lower                # and ends within 2 % of it
    assert hist[-1] <= min(hist) * 1.001          # without wandering back up


def test_lambda_weighted_update_is_inert_at_sigma_tau_one():
    """The historical expression (numerator weight lamda) coincides with the derived one
    (weight mu) when sigma*tau == 1, so historical canonical results are unaffected."""
    f, known = _problem(5)
    for sweep in ("forward", "symmetric"):
        a = pdr_inpaint(f, known, iters=15, sigma=14, tau=1 / 14, sweep=sweep, mu_weighted=False)
        b = pdr_inpaint(f, known, iters=15, sigma=14, tau=1 / 14, sweep=sweep, mu_weighted=True)
        assert np.array_equal(a.u_dr, b.u_dr) and np.array_equal(a.u, b.u)


@pytest.mark.parametrize("sigma_tau", [0.5, 2.0, 4.0])
def test_regression_mu_weighted_update_is_needed_away_from_sigma_tau_one(sigma_tau):
    """With sigma*tau != 1 the corrected iteration still reaches the exact analytic optimum
    (rows*|b-a|), because it solves the intended linear system; the historical lamda-weighted
    expression solves a different one and blows up. Fails if the update is reverted to `lamda*ns`."""
    f, known, lower = _strip_problem()
    ok = pdr_inpaint(f, known, iters=1500, sigma=14, tau=sigma_tau / 14, sweep="symmetric",
                     mu_weighted=True)
    assert tv_energy(ok.u) == pytest.approx(lower, rel=1e-6)
    with np.errstate(all="ignore"):
        bad = pdr_inpaint(f, known, iters=1500, sigma=14, tau=sigma_tau / 14, sweep="symmetric",
                          mu_weighted=False)
        e_bad = tv_energy(bad.u)
    assert not np.isfinite(e_bad) or e_bad > 1.01 * lower


def test_default_solver_is_step_size_consistent():
    """The minimiser must not depend on the step-size product sigma*tau."""
    f, known, lower = _strip_problem()
    energies = [tv_energy(pdr_inpaint(f, known, iters=1500, sigma=14, tau=st / 14).u) for st in (0.5, 1.0, 2.0)]
    assert max(energies) - min(energies) < 1e-6 * lower
