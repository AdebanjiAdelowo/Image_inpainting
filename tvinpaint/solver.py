"""Preconditioned Douglas-Rachford (Bredies & Sun 2014) for hard-constrained TV inpainting.

Problem:   min_u  ||grad u||_{2,1}   subject to   u = f on the known set.

`pdr_inpaint` is the verified implementation. Its defaults differ from the historical notebooks in
three documented ways (docs/Image_Inpainting_Technical_Documentation.md, Sections 7.6.3, 8.7, 9.8):

  sweep       "symmetric" (red-black-red half-sweeps, a self-adjoint and hence feasible
              preconditioner) instead of the notebooks' forward red-black sweep, which is not
              symmetric despite the name `sym_red_black_gauss_seidel`;
  mu_weighted the neighbour weight in the Gauss-Seidel update is mu, as derived from
              (lamda*I - mu*Laplacian) u = b; the notebooks use lamda, which coincides with mu only
              when sigma*tau == 1 (the historical configuration), so results at sigma*tau == 1 are
              unaffected and results elsewhere were wrong;
  result.u    the feasible iterate u_test = P_C(2u - u_bar), which satisfies u == f on the known
              pixels exactly and converges to the same limit (Bredies & Sun, Remark 2.4); the
              notebooks returned the raw Douglas-Rachford iterate, which satisfies the constraint
              only in the limit and is kept here as `result.u_dr`.

`legacy=True` reproduces the notebooks bit for bit (read the historical result from `result.u_dr`).
"""
from dataclasses import dataclass, field

import numpy as np

from .operators import (divergence, gradient, neighbor_sum, neighbour_counts,
                        red_black_masks)


def prox_dual_ball(p, radius):
    """Project the dual field p onto {|p|_2 <= radius} pointwise (prox of F*)."""
    norm = np.maximum(np.sqrt(np.sum(p ** 2, axis=0)) / radius, 1)
    return p / norm


def prox_data(u, f, known):
    """Projection onto {u = f on known}: pin known pixels, leave the hole free (prox of G)."""
    result = u.copy()
    result[known] = f[known]
    return result


def red_black_gauss_seidel(u, lamda, mu, b, n_sweeps, n_nbr, mask_red, mask_black,
                           sweep="symmetric", mu_weighted=True):
    """Red-black Gauss-Seidel for (lamda*I - mu*Laplacian) u = b.

    sweep="forward":   one sweep is red then black (what the notebooks do; not self-adjoint).
    sweep="symmetric": one sweep is red, black, red (self-adjoint, a feasible preconditioner).
    mu_weighted=False: neighbour weight `lamda` in the update (notebook expression, exact only
                       when lamda == mu).
    """
    weight = mu if mu_weighted else lamda
    u = u.copy()
    denom = lamda + n_nbr * mu
    for _ in range(n_sweeps):
        ns = neighbor_sum(u)
        u_new = (b + weight * ns) / denom
        u[mask_red] = u_new[mask_red]

        ns = neighbor_sum(u)
        u_new = (b + weight * ns) / denom
        u[mask_black] = u_new[mask_black]

        if sweep == "symmetric":
            ns = neighbor_sum(u)
            u_new = (b + weight * ns) / denom
            u[mask_red] = u_new[mask_red]
    return u


@dataclass
class PDRResult:
    u: np.ndarray       # the solution: feasible iterate, u == f on the known pixels exactly
    u_dr: np.ndarray    # raw Douglas-Rachford primal iterate (what the notebooks returned)
    p: np.ndarray
    u_bar: np.ndarray
    p_bar: np.ndarray
    iters: int
    history: dict = field(default_factory=dict)


def pdr_inpaint(f, known, *, iters=200, n_sweeps=3, sigma=14, tau=None, alpha=1.0, init=None,
                legacy=False, sweep=None, mu_weighted=None, callback=None):
    """Run `iters` preconditioned Douglas-Rachford iterations and return a `PDRResult`.

    f      : image; only the values on `known` are data. The hole values enter only through the
             warm start `init`, which defaults to `f` as in the notebooks (hole = 255 there).
    known  : boolean array, True where f is trusted.
    sigma, tau : the notebook's step parameters. Only sigma*tau enters the linear system and
             alpha/tau is the dual-ball radius; the minimiser does not depend on either.
    legacy : True reproduces the notebooks (forward sweep, lamda-weighted update); take the
             historical result from `result.u_dr`. Cannot be combined with `sweep`/`mu_weighted`.
    sweep, mu_weighted : ablation switches (defaults "symmetric" and True); set only to isolate
             the effect of one correction.
    callback(k, u_dr, u, p) is called after each iteration (k = 1..iters) if given.
    """
    if legacy:
        if sweep is not None or mu_weighted is not None:
            raise ValueError("legacy=True fixes sweep='forward' and mu_weighted=False")
        sweep, mu_weighted = "forward", False
    else:
        sweep = "symmetric" if sweep is None else sweep
        mu_weighted = True if mu_weighted is None else mu_weighted
    if sweep not in ("forward", "symmetric"):
        raise ValueError("sweep must be 'forward' or 'symmetric'")

    f = np.asarray(f, dtype=np.float64)
    known = np.asarray(known, dtype=bool)
    tau = 1 / sigma if tau is None else tau
    lamda = 1
    mu = (sigma * tau) ** 2
    xdim, ydim = f.shape
    n_nbr = neighbour_counts(f.shape)
    mask_red, mask_black = red_black_masks(f.shape)

    u = (f if init is None else np.asarray(init, dtype=np.float64)).copy()
    u_bar = u.copy()
    p = np.zeros((2, xdim, ydim), dtype=np.float64)
    p_bar = p.copy()
    u_test = prox_data(u, f, known)

    for k in range(iters):
        b = u_bar + sigma * tau * divergence(p_bar)
        u = red_black_gauss_seidel(u, lamda, mu, b, n_sweeps, n_nbr, mask_red, mask_black,
                                   sweep=sweep, mu_weighted=mu_weighted)
        p = p_bar + sigma * tau * gradient(u)
        u_test = prox_data(2 * u - u_bar, f, known)
        u_bar = u_bar + u_test - u
        p_test = prox_dual_ball(2 * p - p_bar, alpha / tau)
        p_bar = p_bar + p_test - p
        if callback is not None:
            callback(k + 1, u, u_test, p)

    return PDRResult(u=u_test, u_dr=u, p=p, u_bar=u_bar, p_bar=p_bar, iters=iters)
