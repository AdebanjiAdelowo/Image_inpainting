"""Scope-boundary check: what the hard-constrained model does when the known pixels are noisy.

The model treats the known pixels as exact (no fidelity/regularisation trade-off), so noise on
them is reproduced verbatim outside the hole. This script only *measures* that documented
limitation; it does not add a penalised (noise-aware) variant.

Observation: known pixels = truth + N(0, s^2) (unclipped float), hole filled with 255.
Metrics are against the clean truth. Canonical mask, shipped TV configuration.
"""
import csv
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np  # noqa: E402

from tvinpaint import baselines, data, metrics  # noqa: E402
from tvinpaint.solver import pdr_inpaint  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "noise_known_pixels.csv")
imgs = data.evaluation_images()
hole = data.make_mask("canonical", data.SHAPE, 0)
known = ~hole
rows = []
for name in ["camera", "astronaut", "phantom", "smooth"]:
    truth = imgs[name]
    for s in [0, 5, 15, 30]:
        for seed in ([0] if s == 0 else [0, 1, 2]):
            noise = np.random.default_rng(1000 + seed).normal(0, s, truth.shape) if s else 0.0
            f = truth + noise
            f[hole] = 255.0
            outs = {"noisy_observation": f, "harmonic": baselines.harmonic_inpaint(f, known),
                    "biharmonic": baselines.biharmonic_inpaint(f, known),
                    "tv_shipped": pdr_inpaint(f, known, legacy=True).u_dr}
            for m, rec in outs.items():
                rc = np.clip(rec, 0, 255)
                rows.append(dict(image=name, noise_sigma=s, noise_seed=seed, method=m,
                                 psnr_hole=metrics.psnr(rc, truth, hole),
                                 rmse_hole=float(np.sqrt(metrics.mse(rc, truth, hole))),
                                 psnr_known=metrics.psnr(rc, truth, known),
                                 rmse_known=float(np.sqrt(metrics.mse(rc, truth, known))),
                                 psnr_full=metrics.psnr(rc, truth)))
    print(name, flush=True)
with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, lineterminator="\n", fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print("wrote", OUT, len(rows))
