"""Baselines that use exactly the same corrupted input f and known-pixel set as the TV solver."""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from .operators import neighbour_counts


def damaged(f, known):
    """No restoration: the observation as given (hole left at its fill value)."""
    return f.copy()


def mean_fill(f, known):
    """Trivial constant fill with the mean of the known pixels."""
    out = f.copy()
    out[~known] = f[known].mean()
    return out


def _neumann_laplacian(shape):
    """Sparse L = -div(grad) = k_ij u_ij - sum of 4-neighbours, the same operator as in the solver."""
    M, N = shape
    idx = np.arange(M * N).reshape(shape)
    rows, cols = [], []
    for a, b in ((idx[:-1, :], idx[1:, :]), (idx[:, :-1], idx[:, 1:])):
        rows += [a.ravel(), b.ravel()]
        cols += [b.ravel(), a.ravel()]
    rows, cols = np.concatenate(rows), np.concatenate(cols)
    A = sp.csr_matrix((np.ones(rows.size), (rows, cols)), shape=(M * N, M * N))
    D = sp.diags(neighbour_counts(shape).ravel())
    return (D - A).tocsr()


def harmonic_inpaint(f, known):
    """min sum |grad u|^2  s.t.  u = f on known, i.e. the quadratic (H1/Tikhonov-type) counterpart
    of the TV problem with the identical discrete gradient. Solved exactly: L_hh u_h = -L_hk f_k."""
    shape = f.shape
    L = _neumann_laplacian(shape)
    h = np.flatnonzero(~known.ravel())
    k = np.flatnonzero(known.ravel())
    rhs = -(L[h][:, k] @ f.ravel()[k])
    uh = spla.spsolve(L[h][:, h].tocsc(), rhs)
    out = f.copy().ravel()
    out[h] = uh
    return out.reshape(shape)


def biharmonic_inpaint(f, known):
    """External reference implementation (scikit-image, Damelin & Hoang 2018). Different
    discretisation from the solver, so it is a reference baseline, not an exact counterpart."""
    from skimage.restoration import inpaint_biharmonic
    return inpaint_biharmonic(f, ~known)
