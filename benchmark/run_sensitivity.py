"""Parameter-sensitivity diagnostics on HELD-OUT development images (moon, coins).

Nothing here selects a parameter: the shipped configuration stays frozen for the evaluation
benchmark. Because the hard-constrained model has no regularisation weight (its minimiser is
independent of alpha), the parameters that matter are the ones of the *iteration*:
  S1  sigma            (tau = 1/sigma, so sigma*tau = 1; sets the dual-ball radius alpha*sigma)
  S2  inner sweeps     n_for_gauss
  S3  iteration budget (how far from the converged solution the shipped 200 iterations are)
  S4  sigma*tau != 1   (the latent lambda/mu inner-solver defect, shipped vs corrected)
  S5  warm start       (white hole as shipped vs known-mean vs harmonic)
"""
import csv
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np  # noqa: E402

from tvinpaint import baselines, data, metrics  # noqa: E402
from tvinpaint.operators import tv_energy  # noqa: E402
from tvinpaint.solver import pdr_inpaint  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "sensitivity_dev.csv")
dev = data.development_images()
CASES = {
    "moon+canonical": (dev["moon"], data.make_mask("canonical", data.SHAPE, 0)),
    "moon+blocks32": (dev["moon"], data.make_mask("blocks32", data.SHAPE, 100)),
    "coins+blocks32": (dev["coins"], data.make_mask("blocks32", dev["coins"].shape, 100)),
}
rows = []


def rec_metrics(exp, case, truth, hole, param, value, rec_u, rec_ut, rt=None, extra=None):
    ru = np.clip(rec_u, 0, 255)
    d = dict(experiment=exp, case=case, param=param, value=value,
             rmse_hole_u=float(np.sqrt(metrics.mse(ru, truth, hole))),
             psnr_hole_u=metrics.psnr(ru, truth, hole),
             rmse_hole_utest=float(np.sqrt(metrics.mse(np.clip(rec_ut, 0, 255), truth, hole))),
             tv_utest=tv_energy(rec_ut), hole_mean_u=float(rec_u[hole].mean()),
             truth_hole_mean=float(truth[hole].mean()), finite=bool(np.isfinite(rec_u).all()),
             runtime_s=rt)
    d.update(extra or {})
    rows.append(d)
    return d


def run(exp, case, param, value, truth, hole, **kw):
    if "sweep" not in kw and "mu_weighted" not in kw:
        kw["legacy"] = True                       # sensitivity is reported for the historical solver
    f = data.damage(truth, hole)
    t = time.perf_counter()
    with np.errstate(all="ignore"):
        r = pdr_inpaint(f, ~hole, **kw)
    dt = time.perf_counter() - t
    return rec_metrics(exp, case, truth, hole, param, value, r.u_dr, r.u, dt), r


for case, (truth, hole) in CASES.items():
    print(case, flush=True)
    for sigma in [2, 5, 8, 14, 25, 50]:                                   # S1
        run("S1_sigma", case, "sigma", sigma, truth, hole, sigma=sigma)
    for n in [1, 2, 3, 5, 10]:                                            # S2
        run("S2_sweeps", case, "n_sweeps", n, truth, hole, n_sweeps=n)
    # S3: iteration budget, shipped forward sweep, checkpoints from a single 2000-iteration run
    f = data.damage(truth, hole)
    marks = [10, 25, 50, 100, 200, 300, 500, 1000, 2000]
    snaps = {}
    def cb(k, u, ut, p, snaps=snaps, marks=marks):
        if k in marks:
            snaps[k] = (u.copy(), ut.copy())
    r = pdr_inpaint(f, ~hole, iters=2000, legacy=True, callback=cb)
    for k in marks:
        d = rec_metrics("S3_iterations", case, truth, hole, "iters", k, *snaps[k])
        d["rel_dist_to_2000"] = float(np.linalg.norm(snaps[k][1] - snaps[2000][1]) / np.linalg.norm(snaps[2000][1]))
    # S5: warm start
    inits = {"white(shipped)": None, "known-mean": baselines.mean_fill(f, ~hole),
             "harmonic": baselines.harmonic_inpaint(f, ~hole)}
    for name, init in inits.items():
        run("S5_init", case, "init", name, truth, hole, init=init)

# S4: sigma*tau != 1, on one case only
truth, hole = CASES["moon+blocks32"]
for st in [0.25, 0.5, 1.0, 2.0, 4.0]:
    for mw in (False, True):
        run("S4_sigma_tau", "moon+blocks32", "sigma*tau|mu_weighted", f"{st}|{mw}", truth, hole,
            sigma=14, tau=st / 14, sweep="forward", mu_weighted=mw)

with open(OUT, "w", newline="") as fh:
    keys = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("experiment", "case", "param", "value"), k))
    w = csv.DictWriter(fh, lineterminator="\n", fieldnames=keys)
    w.writeheader()
    w.writerows(rows)
print("wrote", OUT, len(rows), "rows")
