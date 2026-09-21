"""Frozen evaluation benchmark: 5 images x 19 masks x 8 methods, ground truth known.

Protocol (fixed before any evaluation-set result was seen, nothing is tuned on these images):
  * `tv_shipped` is the historical notebook configuration (pdr_inpaint(..., legacy=True), raw DR
    iterate `u_dr`): sigma=14, tau=1/14, 3 inner sweeps, 200 iterations, warm start from the damaged
    image (hole filled with 255). `tv_shipped_feasible` is the same run's feasible iterate,
    `tv_corrected` is the verified default solver at 200 iterations, `tv_converged` at 1500.
  * Metrics are computed on the reconstruction clipped to [0, 255], data range 255, in float.
  * Headline metric is PSNR on the hole pixels only (known pixels are constrained to the data).

Usage:  python benchmark/run_benchmark.py [--workers 4] [--out benchmark/results] [--limit N]
"""
import argparse
import csv
import json
import os
import platform
import subprocess
import sys
import time
from multiprocessing import Pool

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np  # noqa: E402

from tvinpaint import baselines, data, metrics  # noqa: E402
from tvinpaint.operators import tv_energy  # noqa: E402
from tvinpaint.solver import pdr_inpaint  # noqa: E402

CONFIG = dict(sigma=14, tau_rule="1/sigma", n_sweeps=3, iters=200, converged_iters=1500,
              init="damaged image (hole = 255)", data_range=255.0, area_frac=0.1623,
              trace_iters=[10, 25, 50, 100, 200, 300, 500, 750, 1000, 1500])
MASKS = [("canonical", [0])] + [(k, [0, 1, 2]) for k in
                                ["dropout", "scratch", "blocks8", "blocks16", "blocks32", "blocks64"]]
SAVE_RECON_SEED0 = True


def _row(case, method, rec, truth, hole, known, f, runtime, iters, sweep, returns):
    rec_c = np.clip(rec, 0, 255)
    ssim_full, ssim_hole = metrics.ssim_full_and_hole(rec_c, truth, hole)
    row = dict(case, method=method, iters=iters, sweep=sweep, returns=returns,
               runtime_s=runtime,
               rmse_hole=float(np.sqrt(metrics.mse(rec_c, truth, hole))),
               psnr_hole=metrics.psnr(rec_c, truth, hole),
               rmse_hole_unclipped=float(np.sqrt(metrics.mse(rec, truth, hole))),
               psnr_full=metrics.psnr(rec_c, truth), ssim_full=ssim_full, ssim_hole=ssim_hole,
               tv_out=tv_energy(rec_c), tv_truth=tv_energy(truth),
               known_violation=float(np.abs(rec[known] - f[known]).max()),
               out_of_range_frac_hole=float(((rec[hole] < 0) | (rec[hole] > 255)).mean()))
    row.update(metrics.hole_diagnostics(rec_c, truth, hole))
    return row


def run_case(args):
    image_name, kind, seed = args
    truth = data.evaluation_images()[image_name]
    hole = data.make_mask(kind, data.SHAPE, seed, CONFIG["area_frac"])
    known = ~hole
    f = data.damage(truth, hole)
    case = dict(image=image_name, mask=kind, seed=seed, hole_frac=float(hole.mean()))
    rows, dist_rows, trace_rows, recons = [], [], [], {}

    def add(method, rec, runtime, iters, sweep, returns, keep_dist=False):
        rows.append(_row(case, method, rec, truth, hole, known, f, runtime, iters, sweep, returns))
        recons[method] = np.clip(rec, 0, 255).astype(np.float32)
        if keep_dist:
            for lo, hi, n, r in metrics.error_by_distance(np.clip(rec, 0, 255), truth, hole):
                dist_rows.append(dict(case, method=method, bin_lo=lo, bin_hi=hi, n=n, rmse=r))

    add("damaged", baselines.damaged(f, known), 0.0, 0, "", "")
    add("meanfill", baselines.mean_fill(f, known), 0.0, 0, "", "")
    t = time.perf_counter(); h = baselines.harmonic_inpaint(f, known); dt = time.perf_counter() - t
    add("harmonic", h, dt, 0, "", "exact sparse solve", True)
    t = time.perf_counter(); b = baselines.biharmonic_inpaint(f, known); dt = time.perf_counter() - t
    add("biharmonic", b, dt, 0, "", "skimage", True)

    t = time.perf_counter()
    r = pdr_inpaint(f, known, iters=CONFIG["iters"], n_sweeps=CONFIG["n_sweeps"], sigma=CONFIG["sigma"],
                    legacy=True)
    dt = time.perf_counter() - t
    add("tv_shipped", r.u_dr, dt, 200, "forward", "u", True)                 # historical notebook output
    add("tv_shipped_feasible", r.u, dt, 200, "forward", "u_test")            # same run, feasible iterate

    t = time.perf_counter()
    r = pdr_inpaint(f, known, iters=CONFIG["iters"], n_sweeps=CONFIG["n_sweeps"], sigma=CONFIG["sigma"])
    dt = time.perf_counter() - t
    add("tv_corrected", r.u, dt, 200, "symmetric", "u_test")                 # verified default, 200 it

    snaps, prev = {}, [f.copy()]
    stats = {}

    def cb(k, u, ut, p):
        if k in CONFIG["trace_iters"]:
            snaps[k] = ut.copy()
            stats[k] = (tv_energy(ut), float(np.linalg.norm(u - prev[0]) / np.linalg.norm(u)))
        prev[0] = u

    t = time.perf_counter()
    r = pdr_inpaint(f, known, iters=CONFIG["converged_iters"], n_sweeps=CONFIG["n_sweeps"],
                    sigma=CONFIG["sigma"], callback=cb)
    dt = time.perf_counter() - t
    add("tv_converged", r.u, dt, CONFIG["converged_iters"], "symmetric", "u_test", True)
    ref = r.u
    for k, ut in sorted(snaps.items()):
        c = np.clip(ut, 0, 255)
        trace_rows.append(dict(case, k=k, tv_energy=stats[k][0], rel_change=stats[k][1],
                               rel_dist_to_ref=float(np.linalg.norm(ut - ref) / np.linalg.norm(ref)),
                               rmse_hole=float(np.sqrt(metrics.mse(c, truth, hole))),
                               psnr_hole=metrics.psnr(c, truth, hole)))
    return rows, dist_rows, trace_rows, (case, recons if seed == 0 else None)


def _write_csv(path, rows):
    keys = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, lineterminator="\n", fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"))
    ap.add_argument("--recon-dir", default=None, help="optional: save seed-0 reconstructions (npz) here")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    cases = [(im, kind, s) for s in (0, 1, 2) for kind, seeds in MASKS if s in seeds
             for im in data.evaluation_images()]
    if a.limit:
        cases = cases[:a.limit]
    print(f"{len(cases)} cases, {a.workers} workers", flush=True)
    t0 = time.time()
    all_rows, all_dist, all_trace = [], [], []
    with Pool(a.workers) as pool:
        for i, (rows, dist_rows, trace_rows, (case, recons)) in enumerate(pool.imap_unordered(run_case, cases)):
            all_rows += rows
            all_dist += dist_rows
            all_trace += trace_rows
            if a.recon_dir and recons is not None:
                os.makedirs(a.recon_dir, exist_ok=True)
                np.savez_compressed(os.path.join(a.recon_dir, f"{case['image']}__{case['mask']}__s{case['seed']}.npz"),
                                    **recons)
            print(f"[{i + 1}/{len(cases)}] {case['image']:9s} {case['mask']:9s} s{case['seed']}  "
                  f"{time.time() - t0:6.0f}s elapsed", flush=True)

    key = lambda r: (r["image"], r["mask"], r["seed"])
    for lst in (all_rows, all_dist, all_trace):
        lst.sort(key=lambda r: key(r) + (r.get("method", ""), r.get("bin_lo", 0), r.get("k", 0)))
    _write_csv(os.path.join(a.out, "benchmark_results.csv"), all_rows)
    _write_csv(os.path.join(a.out, "error_by_distance.csv"), all_dist)
    _write_csv(os.path.join(a.out, "convergence_trace.csv"), all_trace)
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).decode().strip()
    except Exception:
        sha = "unknown"
    import scipy, skimage
    meta = dict(config=CONFIG, masks=MASKS, n_cases=len(cases), wall_time_s=time.time() - t0,
                workers=a.workers, load_average_at_end=os.getloadavg(),
                python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                skimage=skimage.__version__, platform=platform.platform(), machine=platform.machine(),
                repo_head=sha)
    json.dump(meta, open(os.path.join(a.out, "run_metadata.json"), "w"), indent=2)
    print("done", round(time.time() - t0), "s", flush=True)


if __name__ == "__main__":
    main()
