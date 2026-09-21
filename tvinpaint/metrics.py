"""Metrics. Every image metric takes an explicit data range (255 for 8-bit-valued images).

Whole-image PSNR/SSIM are inflated by the known pixels, which the constraint keeps (almost)
exact, so the headline metric is computed on the hole pixels only.
"""
import numpy as np
from scipy import ndimage
from skimage.metrics import structural_similarity

from .operators import gradient

DATA_RANGE = 255.0


def mse(a, b, mask=None):
    d = (a - b) ** 2
    return float(d.mean() if mask is None else d[mask].mean())


def psnr_from_mse(m, data_range=DATA_RANGE):
    return float("inf") if m == 0 else float(10 * np.log10(data_range ** 2 / m))


def psnr(a, b, mask=None, data_range=DATA_RANGE):
    return psnr_from_mse(mse(a, b, mask), data_range)


def ssim_full_and_hole(a, b, hole, data_range=DATA_RANGE):
    """Mean SSIM over the whole image, and the mean of the SSIM map over the hole pixels."""
    val, smap = structural_similarity(a, b, data_range=data_range, full=True)
    return float(val), float(smap[hole].mean())


def grad_mag(u):
    g = gradient(u)
    return np.sqrt(g[0] ** 2 + g[1] ** 2)


def laplacian_energy(u):
    lap = ndimage.laplace(u, mode="nearest")
    return lap ** 2


def hole_diagnostics(rec, truth, hole):
    """Failure-mode diagnostics, all restricted to the hole pixels.

    edge_retention   : sum |grad rec| / sum |grad truth| over the hole pixels whose truth gradient
                       is in the top decile (edge band); 1 means edges are as strong as the truth
    grad_ratio       : sum |grad rec| / sum |grad truth| over all hole pixels
    hf_retention     : Laplacian energy of rec / that of truth over the hole (texture retention)
    jump_conc        : share of the hole's total variation carried by its top 1 % gradients
                       (large for staircased, few-large-jumps fields)
    flat_frac        : fraction of hole pixels with gradient below 10 % of the truth's median
                       gradient magnitude over the hole (near-zero-gradient plateaus)
    """
    gr, gt = grad_mag(rec)[hole], grad_mag(truth)[hole]
    top = gt >= np.quantile(gt, 0.9)
    lr, lt = laplacian_energy(rec)[hole], laplacian_energy(truth)[hole]
    top1 = np.sort(gr)[::-1][: max(1, int(0.01 * gr.size))]
    return {
        "edge_retention": float(gr[top].sum() / gt[top].sum()),
        "grad_ratio": float(gr.sum() / gt.sum()),
        "hf_retention": float(lr.sum() / lt.sum()),
        "jump_conc": float(top1.sum() / gr.sum()),
        "flat_frac": float((gr < 0.1 * np.median(gt)).mean()),
    }


DIST_BINS = [(0, 1), (1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 1e9)]


def error_by_distance(rec, truth, hole):
    """Hole RMSE binned by Euclidean distance to the nearest known pixel."""
    dist = ndimage.distance_transform_edt(hole)
    out = []
    for lo, hi in DIST_BINS:
        sel = hole & (dist > lo) & (dist <= hi)
        if sel.any():
            out.append((lo, hi, int(sel.sum()), float(np.sqrt(mse(rec, truth, sel)))))
    return out
