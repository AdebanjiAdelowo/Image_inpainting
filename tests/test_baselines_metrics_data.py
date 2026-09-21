"""Baselines, metrics (data range, no hidden clipping), masks and the canonical case."""
import numpy as np
import pytest
from scipy import ndimage

from tvinpaint import baselines, data, metrics
from tvinpaint.operators import divergence, gradient


def test_harmonic_reproduces_linear_ramp_and_solves_laplace():
    yy, xx = np.mgrid[0:30, 0:36].astype(float)
    img = 3.0 * xx + 2.0 * yy + 5.0
    known = np.ones(img.shape, dtype=bool)
    known[10:20, 12:24] = False
    f = img.copy()
    f[~known] = 255.0
    h = baselines.harmonic_inpaint(f, known)
    assert np.abs(h - img).max() < 1e-8
    assert np.abs(divergence(gradient(h))[~known]).max() < 1e-8
    assert np.array_equal(h[known], f[known])


def test_baselines_share_the_same_known_pixels_and_input():
    img = data.evaluation_images()["smooth"][:80, :90]
    known = ~data.dropout_mask(img.shape, 0.2, 0)
    f = img.copy()
    f[~known] = 255.0
    for fn in (baselines.damaged, baselines.mean_fill, baselines.harmonic_inpaint):
        assert np.array_equal(fn(f, known)[known], f[known])
    assert np.array_equal(baselines.damaged(f, known), f)
    assert np.allclose(baselines.mean_fill(f, known)[~known], f[known].mean())


def test_psnr_definition_and_data_range():
    a = np.full((10, 10), 100.0)
    assert metrics.psnr(a, a) == float("inf")
    assert metrics.psnr(a, a + 10.0) == pytest.approx(20 * np.log10(255 / 10))
    # scale invariance: rescaling the images together with the data range leaves PSNR unchanged
    x = np.random.default_rng(0).random((10, 10)) * 255
    y = x + np.random.default_rng(1).normal(size=x.shape)
    assert metrics.psnr(x / 255, y / 255, data_range=1.0) == pytest.approx(metrics.psnr(x, y))


def test_metrics_do_not_clip_or_quantise():
    a = np.full((8, 8), 100.0)
    assert metrics.psnr(a + 0.4, a) == pytest.approx(20 * np.log10(255 / 0.4))   # sub-grey-level error kept
    assert metrics.mse(a + 300.0, a) == pytest.approx(300.0 ** 2)                   # out-of-range value kept


def test_masked_metrics_use_only_masked_pixels():
    a = np.zeros((10, 10))
    b = a.copy()
    hole = np.zeros_like(a, dtype=bool)
    hole[2:4, 2:4] = True
    b[hole] = 8.0
    assert metrics.mse(b, a, hole) == 64.0
    assert metrics.mse(b, a) == pytest.approx(64.0 * 4 / 100)


def test_ssim_of_identical_images_is_one():
    x = data.evaluation_images()["camera"][:64, :64]
    hole = np.zeros(x.shape, dtype=bool)
    hole[20:30, 20:30] = True
    full, hole_ssim = metrics.ssim_full_and_hole(x, x, hole)
    assert full == pytest.approx(1.0) and hole_ssim == pytest.approx(1.0)


def test_evaluation_images_share_canonical_shape_and_range():
    for name, im in data.evaluation_images().items():
        assert im.shape == data.SHAPE and im.dtype == np.float64, name
        assert im.min() >= 0 and im.max() <= 255, name
        assert im.max() - im.min() > 100, name       # not a degenerate low-contrast image


def test_masks_are_deterministic_and_area_matched():
    for kind in ["dropout", "scratch", "blocks8", "blocks16", "blocks32", "blocks64"]:
        a = data.make_mask(kind, data.SHAPE, 7)
        b = data.make_mask(kind, data.SHAPE, 7)
        assert np.array_equal(a, b)
        assert not np.array_equal(a, data.make_mask(kind, data.SHAPE, 8))
        assert abs(a.mean() - 0.1623) < 0.005, (kind, a.mean())


def test_canonical_mask_matches_documented_statistics():
    f, hole = data.canonical_image_and_mask()
    assert f.shape == hole.shape == data.SHAPE
    assert hole.sum() == 32202 and (~hole).sum() == 166178
    assert ndimage.label(hole, structure=np.ones((3, 3)))[1] == 13
    assert ndimage.distance_transform_edt(hole).max() == pytest.approx(18.36, abs=0.01)
    assert np.all(f[hole] == 255.0)


def test_error_by_distance_covers_every_hole_pixel_once():
    hole = data.make_mask("blocks16", data.SHAPE, 0)
    rec = np.zeros(data.SHAPE)
    truth = np.ones(data.SHAPE)
    rows = metrics.error_by_distance(rec, truth, hole)
    assert sum(r[2] for r in rows) == hole.sum()
    assert all(r[3] == pytest.approx(1.0) for r in rows)
