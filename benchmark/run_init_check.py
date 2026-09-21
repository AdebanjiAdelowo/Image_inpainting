"""Validity check for the 'converged TV' reference: TV minimisers are not unique, so does the
converged result depend on the warm start?  Compare the converged solution from the shipped
white warm start (already in benchmark_results.csv) with one from a harmonic warm start.
Seed-0 cases: canonical and blocks64, all five evaluation images."""
import csv
import os
import sys
from multiprocessing import Pool

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np  # noqa: E402

from tvinpaint import baselines, data, metrics  # noqa: E402
from tvinpaint.operators import tv_energy  # noqa: E402
from tvinpaint.solver import pdr_inpaint  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "init_check_converged.csv")


def job(a):
    im, kind = a
    truth = data.evaluation_images()[im]
    hole = data.make_mask(kind, data.SHAPE, 0)
    f = data.damage(truth, hole)
    out = {}
    for name, init in [("white", None), ("harmonic", baselines.harmonic_inpaint(f, ~hole))]:
        r = pdr_inpaint(f, ~hole, iters=1500, init=init)
        c = np.clip(r.u, 0, 255)
        out[name] = (c, tv_energy(r.u), metrics.psnr(c, truth, hole))
    d = float(np.linalg.norm((out["white"][0] - out["harmonic"][0])[hole]) / np.linalg.norm(out["white"][0][hole]))
    return dict(image=im, mask=kind, tv_white=out["white"][1], tv_harmonic=out["harmonic"][1],
                rel_tv_diff=(out["white"][1] - out["harmonic"][1]) / out["harmonic"][1],
                psnr_hole_white=out["white"][2], psnr_hole_harmonic=out["harmonic"][2],
                rel_hole_diff_between_minimisers=d)


if __name__ == "__main__":
    cases = [(im, k) for k in ("canonical", "blocks64") for im in ["phantom", "camera", "astronaut", "grass", "smooth"]]
    with Pool(4) as p:
        rows = p.map(job, cases)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, lineterminator="\n", fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})
