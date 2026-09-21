"""Operator identities, proximal operators and the inner linear solver."""
import numpy as np
import pytest

from tvinpaint.operators import (divergence, gradient, neighbor_sum, neighbour_counts,
                                 red_black_masks, tv_energy)
from tvinpaint.solver import prox_data, prox_dual_ball, red_black_gauss_seidel

RNG = np.random.default_rng(0)


def test_gradient_divergence_are_negative_adjoints():
    for shape in [(7, 9), (30, 21), (2, 2)]:
        u = RNG.standard_normal(shape)
        p = RNG.standard_normal((2,) + shape)
        lhs = np.sum(gradient(u) * p)
        rhs = -np.sum(u * divergence(p))
        assert abs(lhs - rhs) < 1e-12 * max(1, abs(lhs))


def test_operator_norm_bound_sqrt8():
    shape = (24, 31)
    u = RNG.standard_normal(shape)
    for _ in range(300):  # power iteration on K^T K = -div grad
        v = -divergence(gradient(u))
        u = v / np.linalg.norm(v)
    est = np.sqrt(np.sum(gradient(u) ** 2))
    assert est <= np.sqrt(8) + 1e-9
    assert est > 2.5  # and it is reasonably tight


def test_neumann_laplacian_identity():
    shape = (13, 17)
    u = RNG.standard_normal(shape)
    lhs = -divergence(gradient(u))
    rhs = neighbour_counts(shape) * u - neighbor_sum(u)
    assert np.abs(lhs - rhs).max() < 1e-12


def test_prox_dual_ball_is_projection():
    p = 5 * RNG.standard_normal((2, 20, 20))
    r = 2.0
    q = prox_dual_ball(p, r)
    assert (np.sqrt((q ** 2).sum(0)) <= r + 1e-12).all()             # feasible
    assert np.allclose(prox_dual_ball(q, r), q, atol=1e-13)           # idempotent
    inside = 0.1 * RNG.standard_normal((2, 20, 20))
    assert np.array_equal(prox_dual_ball(inside, r), inside)          # unchanged inside the ball
    # nearest-point property against random feasible competitors
    d_q = np.sqrt(((p - q) ** 2).sum(0))
    for _ in range(200):
        c = RNG.standard_normal((2, 20, 20))
        c = r * c / np.maximum(np.sqrt((c ** 2).sum(0)), 1)
        assert (np.sqrt(((p - c) ** 2).sum(0)) >= d_q - 1e-12).all()


def test_moreau_identity_isotropic_tv():
    """v = prox_F(v) + prox_{F*}(v) with F = alpha*||.||_{2,1} (group shrinkage) and
    F* the indicator of the pointwise 2-norm ball. This is what makes `prox_dual_ball` the
    correct dual step for *isotropic* TV."""
    alpha = 3.0
    v = 4 * RNG.standard_normal((2, 15, 15))
    nrm = np.sqrt((v ** 2).sum(0))
    shrink = v * np.maximum(1 - alpha / np.maximum(nrm, 1e-300), 0)
    assert np.abs(shrink + prox_dual_ball(v, alpha) - v).max() < 1e-12


def test_prox_data_is_projection_onto_data_set():
    f = RNG.standard_normal((9, 11))
    known = RNG.random((9, 11)) < 0.6
    u = RNG.standard_normal((9, 11))
    z = prox_data(u, f, known)
    assert np.array_equal(z[known], f[known])
    assert np.array_equal(z[~known], u[~known])
    assert np.array_equal(prox_data(z, f, known), z)


def _residual(u, lamda, mu, b):
    shape = u.shape
    lu = lamda * u + mu * (neighbour_counts(shape) * u - neighbor_sum(u))   # (lamda I - mu Delta) u
    return np.linalg.norm(lu - b) / np.linalg.norm(b)


@pytest.mark.parametrize("lamda,mu", [(1, 1), (1, 4), (1, 0.25), (2, 1)])
def test_inner_solver_legacy_versus_mu_weighted(lamda, mu):
    shape = (14, 18)
    b = RNG.standard_normal(shape)
    nbr, red, black = neighbour_counts(shape), *red_black_masks(shape)
    kw = dict(n_sweeps=400, n_nbr=nbr, mask_red=red, mask_black=black)
    corrected = red_black_gauss_seidel(np.zeros(shape), lamda, mu, b, mu_weighted=True, **kw)
    assert _residual(corrected, lamda, mu, b) < 1e-10          # default (symmetric sweep, mu weight)
    with np.errstate(all="ignore"):                            # the historical expression and sweep
        shipped = red_black_gauss_seidel(np.zeros(shape), lamda, mu, b, sweep="forward",
                                         mu_weighted=False, **kw)
    res = _residual(shipped, lamda, mu, b)
    if lamda == mu:
        assert res < 1e-10            # exact for the shipped sigma*tau = 1 configuration
    else:
        assert not res < 1e-3         # wrong (or divergent) whenever lambda != mu


def _gs_preconditioner(sweep, n_sweeps, shape=(6, 5)):
    """Extract M^{-1} of the affine map x -> x + M^{-1}(b - T x) realised by the sweeps."""
    lamda = mu = 1
    nbr, red, black = neighbour_counts(shape), *red_black_masks(shape)
    n = shape[0] * shape[1]

    def T(x):
        u = x.reshape(shape)
        return (lamda * u + mu * (nbr * u - neighbor_sum(u))).ravel()

    Tm = np.stack([T(e) for e in np.eye(n)], axis=1)
    Minv = np.zeros((n, n))
    for j in range(n):
        b = np.eye(n)[j].reshape(shape)
        out = red_black_gauss_seidel(np.zeros(shape), lamda, mu, b, n_sweeps, nbr, red, black,
                                     sweep=sweep, mu_weighted=True)
        Minv[:, j] = out.ravel()
    return Tm, Minv


def test_forward_sweep_is_not_feasible_but_symmetric_sweep_is():
    """Reproduces docs Section 7.6.3: only red-black-red gives a self-adjoint M with M >= T."""
    for sweep, feasible in [("forward", False), ("symmetric", True)]:
        Tm, Minv = _gs_preconditioner(sweep, 1)
        asym = np.linalg.norm(Minv - Minv.T) / np.linalg.norm(Minv)
        M = np.linalg.inv(Minv)
        Ms = (M + M.T) / 2 - Tm
        min_eig = np.linalg.eigvalsh((Ms + Ms.T) / 2).min()
        if feasible:
            assert asym < 1e-12 and min_eig > -1e-10
        else:
            assert asym > 1e-2 and min_eig < -0.1


def test_tv_energy_of_constant_and_step():
    assert tv_energy(np.full((5, 6), 3.0)) == 0
    u = np.zeros((4, 6))
    u[:, 3:] = 10.0
    assert tv_energy(u) == pytest.approx(4 * 10.0)
