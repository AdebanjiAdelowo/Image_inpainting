"""Re-run the repository's canonical experiment (u0.png + lossregion.png, no ground truth) with
BOTH the historical notebook algorithm (legacy=True, raw DR iterate `u_dr`) and the verified solver
(defaults, feasible iterate `u`), and record energies, constraint violation, hole statistics,
runtime and the differences between the two.

Serial timing, 5 repeats; the load average is recorded because runtime is only meaningful
relative to how busy the machine was.
"""
import json
import os
import platform
import subprocess
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np  # noqa: E402

from tvinpaint import baselines, data  # noqa: E402
from tvinpaint.operators import tv_energy  # noqa: E402
from tvinpaint.solver import pdr_inpaint  # noqa: E402

f, hole = data.canonical_image_and_mask()
known = ~hole
out = dict(machine=subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip(),
           platform=platform.platform(), python=platform.python_version(), numpy=np.__version__,
           image_shape=list(f.shape), known=int(known.sum()), unknown=int(hole.sum()),
           config=dict(sigma=14, tau="1/14", n_sweeps=3, iters=200, init="u0.png (hole = 255)"))
out["load_average_before"] = os.getloadavg()

MODES = {"historical": dict(legacy=True), "verified": dict()}
times = {}
for name, kw in MODES.items():
    ts = []
    for _ in range(5):
        t = time.perf_counter()
        pdr_inpaint(f, known, **kw)
        ts.append(time.perf_counter() - t)
    times[name + "_200"] = dict(runs_s=ts, best_s=min(ts), median_s=float(np.median(ts)))
ts = []
for _ in range(5):
    t = time.perf_counter()
    baselines.harmonic_inpaint(f, known)
    ts.append(time.perf_counter() - t)
times["harmonic_exact"] = dict(runs_s=ts, best_s=min(ts), median_s=float(np.median(ts)))
out["timing"] = times
out["load_average_after_timing"] = os.getloadavg()

# one 2000-iteration run per mode; the k=200 snapshots equal a standalone 200-iteration run
marks = [1, 10, 50, 100, 200, 500, 1000, 2000]
snap = {m: {} for m in MODES}
stats = {m: {} for m in MODES}
for name, kw in MODES.items():
    prev = [f.copy()]
    def cb(k, u_dr, u, p, name=name, prev=prev):
        if k in marks:
            snap[name][k] = (u_dr.copy(), u.copy(), p.copy())
            stats[name][k] = float(np.linalg.norm(u_dr - prev[0]) / np.linalg.norm(u_dr))
        prev[0] = u_dr
    pdr_inpaint(f, known, iters=2000, callback=cb, **kw)

ref = snap["verified"][2000][1]                     # verified solver, 2000 iterations
hist_u, hist_feas, hist_p = snap["historical"][200]
ver_u = snap["verified"][200][1]
nrm = lambda a: float(np.linalg.norm(a))


def describe(u, label, p=None):
    d = dict(tv_energy=tv_energy(u), max_known_violation=float(np.abs(u[known] - f[known]).max()),
             u_min=float(u.min()), u_max=float(u.max()), hole_mean=float(u[hole].mean()),
             hole_min=float(u[hole].min()), hole_max=float(u[hole].max()),
             rel_dist_to_verified_2000=nrm(u - ref) / nrm(ref))
    if p is not None:
        d["max_dual_norm"] = float(np.sqrt((p ** 2).sum(0)).max())
    return d


out["results_200_iterations"] = {
    "historical_returned_iterate_u_dr": describe(hist_u, "hist", hist_p),
    "historical_feasible_iterate": describe(hist_feas, "hist_feas"),
    "verified_solution": describe(ver_u, "verified", snap["verified"][200][2]),
}


def diff(a, b):
    d = a - b
    return dict(rel_l2_whole_image=nrm(d) / nrm(a), rel_l2_hole=nrm(d[hole]) / nrm(a[hole]),
                max_abs_hole=float(np.abs(d[hole]).max()), max_abs_known=float(np.abs(d[known]).max()),
                frac_hole_pixels_differing_by_more_than_1=float((np.abs(d[hole]) > 1).mean()),
                tv_energy_difference=tv_energy(a) - tv_energy(b))


out["differences_at_200_iterations"] = {
    "constraint_fix_only__historical_u_dr_vs_historical_feasible": diff(hist_u, hist_feas),
    "sweep_fix_only__historical_feasible_vs_verified": diff(hist_feas, ver_u),
    "both__historical_u_dr_vs_verified": diff(hist_u, ver_u),
}
out["convergence"] = {
    m: {str(k): dict(tv_energy_feasible=tv_energy(snap[m][k][1]), rel_change_of_u_dr=stats[m][k],
                     rel_dist_to_own_2000=nrm(snap[m][k][1] - snap[m][2000][1]) / nrm(snap[m][2000][1]))
        for k in marks} for m in MODES}
out["load_average_end"] = os.getloadavg()

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "canonical_reproduction.json")
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(out, open(path, "w"), indent=2)
print(json.dumps({k: out[k] for k in ("timing", "results_200_iterations", "differences_at_200_iterations",
                                       "load_average_before", "load_average_after_timing")}, indent=1))
