"""The command line entry point runs on the repository's canonical inputs."""
import numpy as np
from PIL import Image

from tvinpaint import data
from tvinpaint.__main__ import main


def test_cli_writes_a_reconstruction_that_keeps_the_known_pixels(tmp_path):
    out = tmp_path / "rec.png"
    u = main(["--iters", "3", "--out", str(out)])
    f, hole = data.canonical_image_and_mask()
    img = np.array(Image.open(out)).astype(float)
    assert img.shape == f.shape
    assert np.array_equal(u[~hole], f[~hole])            # verified mode: exact on known pixels
    assert np.array_equal(img[~hole], f[~hole])          # and therefore in the written file
    assert img[hole].std() > 0                            # the hole was actually processed


def test_cli_legacy_mode_returns_the_raw_iterate(tmp_path):
    u = main(["--iters", "3", "--legacy", "--out", str(tmp_path / "leg.png")])
    f, hole = data.canonical_image_and_mask()
    assert np.abs(u[~hole] - f[~hole]).max() > 0          # raw iterate is not exactly feasible
