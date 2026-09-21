"""Discrete operators on an M x N grid, ported unchanged from the notebooks.

`gradient` is the forward-difference operator K (zero in the last row/column),
`divergence` is -K^T (backward differences), so <grad u, p> = -<u, div p>.
"""
import numpy as np


def gradient(img):
    """Forward finite differences along each axis; zero outside domain boundary."""
    gy = np.zeros_like(img)
    gx = np.zeros_like(img)
    gy[:-1, :] = np.diff(img, axis=0)
    gx[:, :-1] = np.diff(img, axis=1)
    return np.stack([gy, gx])


def divergence(grad):
    """Backward finite differences, the negative adjoint of `gradient`."""
    gy, gx = grad[0], grad[1]
    dy = np.zeros_like(gy)
    dx = np.zeros_like(gx)
    dy[0, :] = gy[0, :]
    dy[1:-1, :] = gy[1:-1, :] - gy[:-2, :]
    dy[-1, :] = -gy[-2, :]
    dx[:, 0] = gx[:, 0]
    dx[:, 1:-1] = gx[:, 1:-1] - gx[:, :-2]
    dx[:, -1] = -gx[:, -2]
    return dy + dx


def neighbor_sum(u):
    """Sum of 4-connected neighbours; zero contribution outside the domain."""
    ns = np.zeros_like(u)
    ns[:-1, :] += u[1:, :]
    ns[1:, :] += u[:-1, :]
    ns[:, :-1] += u[:, 1:]
    ns[:, 1:] += u[:, :-1]
    return ns


def neighbour_counts(shape):
    """Number of 4-connected neighbours per pixel (4 interior, 3 edge, 2 corner)."""
    n_nbr = np.full(shape, 4.0)
    n_nbr[0, :] -= 1
    n_nbr[-1, :] -= 1
    n_nbr[:, 0] -= 1
    n_nbr[:, -1] -= 1
    return n_nbr


def red_black_masks(shape):
    """Checkerboard masks: red is (i+j) even, black is (i+j) odd."""
    mask_red = np.zeros(shape, dtype=bool)
    mask_red[0::2, 0::2] = True
    mask_red[1::2, 1::2] = True
    return mask_red, ~mask_red


def tv_energy(u):
    """Isotropic discrete total variation  sum_ij sqrt(gy^2 + gx^2)  of `u`."""
    g = gradient(u)
    return float(np.sqrt(g[0] ** 2 + g[1] ** 2).sum())
