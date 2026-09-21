"""Command line entry point:  python -m tvinpaint [--iters N] [--legacy] [--out FILE]

Inpaints `u0.png` where `lossregion.png` is white (255 = unknown, 0 = known), the same inputs as
the notebooks, and writes the reconstruction as an 8-bit greyscale PNG.

Default: the verified solver; the written image satisfies u = f on the known pixels exactly.
--legacy: reproduces the historical notebooks (forward sweep, raw Douglas-Rachford iterate).
"""
import argparse
import os
import time

import numpy as np
from PIL import Image

from .data import REPO_DIR, canonical_image_and_mask
from .operators import tv_energy
from .solver import pdr_inpaint


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m tvinpaint", description=__doc__.split("\n")[0])
    ap.add_argument("--image", default=os.path.join(REPO_DIR, "u0.png"))
    ap.add_argument("--mask", default=os.path.join(REPO_DIR, "lossregion.png"))
    ap.add_argument("--iters", type=int, default=200, help="Douglas-Rachford iterations (default 200)")
    ap.add_argument("--legacy", action="store_true", help="reproduce the historical notebook result")
    ap.add_argument("--out", default="reconstruction.png")
    a = ap.parse_args(argv)

    f, hole = canonical_image_and_mask()
    if (a.image, a.mask) != (os.path.join(REPO_DIR, "u0.png"), os.path.join(REPO_DIR, "lossregion.png")):
        f = np.array(Image.open(a.image))
        f = (f[:, :, 0] if f.ndim == 3 else f).astype(np.float64)
        m = np.array(Image.open(a.mask))
        hole = (m[:, :, 0] if m.ndim == 3 else m) == 255
    known = ~hole

    t = time.perf_counter()
    res = pdr_inpaint(f, known, iters=a.iters, legacy=a.legacy)
    dt = time.perf_counter() - t
    u = res.u_dr if a.legacy else res.u
    Image.fromarray(np.clip(np.round(u), 0, 255).astype(np.uint8)).save(a.out)
    print(f"{'legacy (notebook)' if a.legacy else 'verified'} solver, {a.iters} iterations, {dt:.2f} s")
    print(f"TV energy {tv_energy(u):.1f}, max |u - f| on known pixels {np.abs(u[known] - f[known]).max():.3g}")
    print(f"wrote {a.out}")
    return u


if __name__ == "__main__":
    main()
