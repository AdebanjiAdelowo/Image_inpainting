"""Test images and loss masks for the benchmark. Everything is deterministic and offline.

All images are float64 in [0, 255] and share the canonical 436 x 455 shape, so the repository's
own loss mask (`lossregion.png`) can be transplanted onto any of them.
"""
import os

import numpy as np
from PIL import Image
from skimage import color, data, draw, morphology, transform

SHAPE = (436, 455)
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _crop(a, shape=SHAPE):
    """Centre crop of `a` to `shape`."""
    r0 = (a.shape[0] - shape[0]) // 2
    c0 = (a.shape[1] - shape[1]) // 2
    return a[r0:r0 + shape[0], c0:c0 + shape[1]]


def _phantom():
    ph = data.shepp_logan_phantom()
    ph = transform.resize(ph, SHAPE, order=1, anti_aliasing=False, mode="edge")
    return 255.0 * ph


def _smooth():
    """Edge-free synthetic image: a linear ramp plus three Gaussian bumps, range [20, 235]."""
    yy, xx = np.mgrid[0:SHAPE[0], 0:SHAPE[1]].astype(np.float64)
    y, x = yy / SHAPE[0], xx / SHAPE[1]
    g = lambda cy, cx, s: np.exp(-((y - cy) ** 2 + (x - cx) ** 2) / (2 * s ** 2))
    z = 0.35 * x + 0.15 * y + 0.9 * g(0.3, 0.3, 0.12) + 0.7 * g(0.65, 0.7, 0.18) + 0.5 * g(0.8, 0.25, 0.09)
    z = (z - z.min()) / (z.max() - z.min())
    return 20.0 + 215.0 * z


def _gray(rgb):
    return 255.0 * color.rgb2gray(rgb)


def evaluation_images():
    """The five frozen evaluation images."""
    return {
        "phantom": _phantom(),                                   # piecewise constant, TV's best case
        "camera": _crop(data.camera().astype(np.float64)),        # strong edges plus grass texture
        "astronaut": _crop(_gray(data.astronaut())),              # natural image, smooth shading and fabric
        "grass": _crop(data.grass().astype(np.float64)),          # pure texture, no large structure
        "smooth": _smooth(),                                     # edge-free gradients (staircasing probe)
    }


def development_images():
    """Held-out images used only for parameter-sensitivity diagnostics, never for evaluation."""
    moon = _crop(data.moon().astype(np.float64))
    coins = data.coins().astype(np.float64)
    return {"moon": moon, "coins": coins}


def canonical_image_and_mask():
    """The repository's own damaged image and loss mask. There is no ground truth for it."""
    f = np.array(Image.open(os.path.join(REPO_DIR, "u0.png")))[:, :, 0].astype(np.float64)
    m = np.array(Image.open(os.path.join(REPO_DIR, "lossregion.png")))[:, :, 0]
    return f, (m == 255)


def canonical_hole_mask():
    """Boolean hole mask (True = unknown) of the repository's loss region."""
    return canonical_image_and_mask()[1]


def _overlaps(taken, r, c, s, gap):
    r0, c0 = max(r - gap, 0), max(c - gap, 0)
    return taken[r0:r + s + gap, c0:c + s + gap].any()


def block_mask(shape, size, area_frac, seed, margin=8, gap=2):
    """Random non-overlapping size x size squares covering about `area_frac` of the image."""
    rng = np.random.default_rng(seed)
    n = int(round(area_frac * shape[0] * shape[1] / size ** 2))
    hole = np.zeros(shape, dtype=bool)
    placed, tries = 0, 0
    while placed < n:
        tries += 1
        if tries > 200000:
            raise RuntimeError("could not place blocks")
        r = int(rng.integers(margin, shape[0] - margin - size))
        c = int(rng.integers(margin, shape[1] - margin - size))
        if _overlaps(hole, r, c, size, gap):
            continue
        hole[r:r + size, c:c + size] = True
        placed += 1
    return hole


def dropout_mask(shape, area_frac, seed):
    """Exactly round(area_frac * M * N) pixels dropped uniformly at random."""
    rng = np.random.default_rng(seed)
    n = int(round(area_frac * shape[0] * shape[1]))
    flat = np.zeros(shape[0] * shape[1], dtype=bool)
    flat[rng.choice(flat.size, size=n, replace=False)] = True
    return flat.reshape(shape)


def scratch_mask(shape, area_frac, seed, width=2, min_len=40, max_len=200):
    """Random straight scratches of a given pixel width until `area_frac` is reached."""
    rng = np.random.default_rng(seed)
    hole = np.zeros(shape, dtype=bool)
    target = area_frac * shape[0] * shape[1]
    se = np.ones((width, width), dtype=bool)
    while hole.sum() < target:
        r0, c0 = int(rng.integers(0, shape[0])), int(rng.integers(0, shape[1]))
        ang, ln = rng.uniform(0, np.pi), rng.uniform(min_len, max_len)
        r1 = int(np.clip(r0 + ln * np.sin(ang), 0, shape[0] - 1))
        c1 = int(np.clip(c0 + ln * np.cos(ang), 0, shape[1] - 1))
        line = np.zeros(shape, dtype=bool)
        rr, cc = draw.line(r0, c0, r1, c1)
        line[rr, cc] = True
        hole |= morphology.dilation(line, se)
    return hole


def make_mask(kind, shape, seed, area_frac=0.1623):
    """Mask factory. `kind` is 'canonical', 'dropout', 'scratch' or 'blocks<size>'."""
    if kind == "canonical":
        m = canonical_hole_mask()
        if m.shape != shape:
            raise ValueError("canonical mask needs the 436 x 455 canonical shape")
        return m
    if kind == "dropout":
        return dropout_mask(shape, area_frac, seed)
    if kind == "scratch":
        return scratch_mask(shape, area_frac, seed)
    if kind.startswith("blocks"):
        return block_mask(shape, int(kind[len("blocks"):]), area_frac, seed)
    raise ValueError(kind)


def damage(image, hole, fill=255.0):
    """The observation the solvers see: `image` with the hole overwritten by `fill` (white)."""
    f = image.copy()
    f[hole] = fill
    return f
