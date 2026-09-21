"""Figures for the benchmark. Usage: python benchmark/make_figures.py --recon-dir DIR
(reconstructions are re-creatable by run_benchmark.py --recon-dir; they are not committed)."""
import argparse
import csv
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402

from tvinpaint import data  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
FIG = os.path.join(HERE, "figures")
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
COL = {"harmonic": "#2a78d6", "biharmonic": "#1baf7a", "tv_shipped": "#eb6834", "tv_converged": "#4a3aa7"}
LAB = {"harmonic": "Harmonic", "biharmonic": "Biharmonic", "tv_shipped": "TV, shipped (200 it)",
       "tv_converged": "TV, converged (1500 it)"}
MARK = {"harmonic": "s", "biharmonic": "^", "tv_shipped": "o", "tv_converged": "D"}
IMAGES = ["phantom", "camera", "astronaut", "grass", "smooth"]
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb"})


def load(name):
    rows = list(csv.DictReader(open(os.path.join(RES, name))))
    for r in rows:
        for k, v in r.items():
            if k not in ("image", "mask", "method", "sweep", "returns", "experiment", "case", "param", "value"):
                try:
                    r[k] = float(v)
                except (TypeError, ValueError):
                    pass
    return rows


def maxdist():
    return {k: float(np.mean([ndimage.distance_transform_edt(data.make_mask(k, data.SHAPE, s)).max()
                              for s in ([0] if k == "canonical" else [0, 1, 2])]))
            for k in ["canonical", "dropout", "scratch", "blocks8", "blocks16", "blocks32", "blocks64"]}


def fig_comparison(recon_dir, mask="blocks64"):
    truth = data.evaluation_images()
    hole = data.make_mask(mask, data.SHAPE, 0)
    lab, n = ndimage.label(hole)
    cents = ndimage.center_of_mass(hole, lab, range(1, n + 1))
    cy, cx = next((int(y), int(x)) for y, x in cents if 70 < y < data.SHAPE[0] - 70 and 70 < x < data.SHAPE[1] - 70)
    sl = (slice(cy - 56, cy + 56), slice(cx - 56, cx + 56))      # rule: first interior block in raster order
    cols = ["truth", "damaged", "harmonic", "biharmonic", "tv_shipped", "tv_converged"]
    fig, ax = plt.subplots(len(IMAGES), len(cols), figsize=(11, 9.4))
    for i, im in enumerate(IMAGES):
        rec = np.load(os.path.join(recon_dir, f"{im}__{mask}__s0.npz"))
        for j, c in enumerate(cols):
            a = ax[i, j]
            arr = truth[im] if c == "truth" else rec[c]
            a.imshow(arr[sl], cmap="gray", vmin=0, vmax=255, interpolation="nearest")
            a.set_xticks([]); a.set_yticks([]); a.grid(False)
            for s in a.spines.values():
                s.set_visible(False)
            if i == 0:
                a.set_title({"truth": "Ground truth", "damaged": "Damaged input"}.get(c, LAB.get(c)), fontsize=9)
            if j == 0:
                a.set_ylabel(im, fontsize=10)
            if c not in ("truth",):
                m = hole.copy()
                e = float(np.sqrt(((arr.astype(float) - truth[im]) ** 2)[m].mean()))
                psnr = 20 * np.log10(255 / e)
                a.set_xlabel(f"hole PSNR {psnr:.1f} dB", fontsize=8, color=MUTED)
    fig.suptitle(f"Mask '{mask}' (seed 0), crop around one 64x64 hole. All methods see the identical damaged input.",
                 fontsize=10, y=0.995)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_comparison_blocks64.png"), dpi=130)
    plt.close(fig)


def fig_psnr_vs_inradius():
    R = load("benchmark_results.csv")
    md = maxdist()
    fig, axs = plt.subplots(1, 5, figsize=(14, 3.4), sharex=True)
    for a, im in zip(axs, IMAGES):
        for m in COL:
            xs, ys, es = [], [], []
            for k in sorted(["dropout", "scratch", "blocks8", "blocks16", "blocks32", "blocks64"], key=md.get):
                v = [r["psnr_hole"] for r in R if r["image"] == im and r["mask"] == k and r["method"] == m]
                xs.append(md[k]); ys.append(np.mean(v)); es.append(np.std(v))
            a.errorbar(xs, ys, yerr=es, color=COL[m], marker=MARK[m], ms=4.5, lw=1.4, capsize=2, label=LAB[m])
            v = [r["psnr_hole"] for r in R if r["image"] == im and r["mask"] == "canonical" and r["method"] == m]
            a.plot([md["canonical"]], v, marker=MARK[m], ms=7, mfc="none", mec=COL[m], mew=1.5, ls="none")
        a.set_xscale("log"); a.set_title(im, fontsize=10)
        a.set_xlabel("max distance to known pixel (px)")
    axs[0].set_ylabel("PSNR on hole pixels (dB)")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.04))
    fig.suptitle("Hole PSNR at fixed damaged area (16.2 %): filled = synthetic masks (mean +/- sd, 3 seeds), "
                 "hollow = repository's canonical mask", fontsize=9.5, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_psnr_vs_hole_size.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)


def fig_sensitivity():
    S = load("sensitivity_dev.csv")
    cases = ["moon+canonical", "moon+blocks32", "coins+blocks32"]
    cc = dict(zip(cases, ["#2a78d6", "#eb6834", "#4a3aa7"]))
    mk = dict(zip(cases, ["o", "s", "^"]))
    fig, axs = plt.subplots(1, 3, figsize=(12.5, 3.6))
    for c in cases:
        for a, exp, xkey in [(axs[0], "S1_sigma", "value"), (axs[1], "S3_iterations", "value"),
                             (axs[2], "S2_sweeps", "value")]:
            sub = [s for s in S if s["experiment"] == exp and s["case"] == c]
            x = [float(s["value"]) for s in sub]
            y = [s["rmse_hole_utest"] for s in sub]
            a.plot(x, y, color=cc[c], marker=mk[c], ms=4.5, lw=1.4, label=c)
    for a, t, xl in [(axs[0], "sigma (tau = 1/sigma), 200 iterations", "sigma"),
                     (axs[1], "iteration budget (shipped sigma, 3 sweeps)", "iterations"),
                     (axs[2], "inner Gauss-Seidel sweeps, 200 iterations", "sweeps")]:
        a.set_title(t, fontsize=9.5); a.set_xlabel(xl); a.set_yscale("log")
    axs[1].set_xscale("log")
    axs[0].set_xscale("log")
    axs[0].set_xticks([2, 5, 14, 25, 50]); axs[0].set_xticklabels(["2", "5", "14", "25", "50"]); axs[0].minorticks_off()
    axs[0].axvline(14, color=MUTED, lw=0.8, ls="--"); axs[1].axvline(200, color=MUTED, lw=0.8, ls="--")
    axs[2].axvline(3, color=MUTED, lw=0.8, ls="--")
    axs[0].set_ylabel("RMSE on hole pixels (grey levels)")
    axs[0].legend(frameon=False, fontsize=8)
    fig.suptitle("Held-out development images only. Dashed line = shipped setting. "
                 "The model's minimiser does not depend on sigma; these curves show iteration behaviour.",
                 fontsize=9.5, y=1.03)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_sensitivity_dev.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)


def fig_convergence():
    T = load("convergence_trace.csv")
    md = maxdist()
    order = sorted(md, key=md.get)
    ks = sorted({int(t["k"]) for t in T})
    shades = plt.cm.Blues(np.linspace(0.3, 0.95, len(order)))
    tr = defaultdict(dict)
    for t in T:
        tr[(t["image"], t["mask"], int(t["seed"]))][int(t["k"])] = t
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.6))
    for col, k in zip(shades, order):
        cs = [c for c in tr if c[1] == k]
        axs[0].plot(ks[:-1], [np.median([tr[c][kk]["rel_dist_to_ref"] for c in cs]) for kk in ks[:-1]], color=col, marker="o",
                    ms=3.5, lw=1.4, label=f"{k} ({md[k]:.0f} px)")
        axs[1].plot(ks, [np.mean([tr[c][kk]["psnr_hole"] - tr[c][1500]["psnr_hole"] for c in cs]) for kk in ks],
                    color=col, marker="o", ms=3.5, lw=1.4)
    for a in axs:
        a.set_xscale("log"); a.set_xlabel("iteration k"); a.axvline(200, color=MUTED, lw=0.8, ls="--")
    axs[0].set_yscale("log")
    axs[0].set_ylabel("relative distance to 1500-iteration result")
    axs[1].set_ylabel("hole PSNR minus PSNR at k=1500 (dB)")
    axs[1].axhline(0, color=MUTED, lw=0.8)
    axs[0].legend(frameon=False, fontsize=7.5, title="mask (max distance)", title_fontsize=8)
    fig.suptitle("Convergence of the shipped-style iteration by hole size (symmetric variant, all images). "
                 "Dashed = shipped 200 iterations.", fontsize=9.5, y=1.03)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_convergence.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)


def fig_failure_modes(recon_dir):
    R = load("benchmark_results.csv")
    D = load("error_by_distance.csv")
    truth = data.evaluation_images()
    from matplotlib.colors import LinearSegmentedColormap
    fig = plt.figure(figsize=(11.5, 7.6))
    gs = fig.add_gridspec(2, 2)
    axs = np.empty((2, 2), dtype=object)
    for (i, j) in [(0, 1), (1, 0), (1, 1)]:
        axs[i, j] = fig.add_subplot(gs[i, j])
    # (a) cross-section through a 64x64 hole of the smooth image
    hole = data.make_mask("blocks64", data.SHAPE, 0)
    lab, n = ndimage.label(hole)
    cents = ndimage.center_of_mass(hole, lab, range(1, n + 1))
    cy, cx = next((int(y), int(x)) for y, x in cents if 70 < y < data.SHAPE[0] - 70 and 70 < x < data.SHAPE[1] - 70)
    rec = np.load(os.path.join(recon_dir, "smooth__blocks64__s0.npz"))
    sub = gs[0, 0].subgridspec(2, 3, width_ratios=[1, 1, 0.06], wspace=0.1, hspace=0.55)
    lab_all, nb = ndimage.label(hole)
    err = {m: rec[m].astype(float) - truth["smooth"] for m in ["harmonic", "tv_converged"]}
    rm = lambda m, b: float(np.sqrt((err[m][lab_all == b] ** 2).mean()))
    first = int(lab_all[cy, cx])
    worst = max(range(1, nb + 1), key=lambda b: rm("tv_converged", b) - rm("harmonic", b))
    div = LinearSegmentedColormap.from_list("div", ["#2a78d6", "#e6e5e1", "#eb6834"])
    wins = sum(rm("tv_converged", b) < rm("harmonic", b) for b in range(1, nb + 1))
    for r, (b, tag) in enumerate([(first, "block A: first interior block (rule fixed in advance)"),
                                  (worst, "block B: largest TV - harmonic RMSE gap (picked after the fact)")]):
        ys, xs_ = np.where(lab_all == b)
        sl = (slice(ys.min() - 4, ys.max() + 5), slice(xs_.min() - 4, xs_.max() + 5))
        lim = max(np.abs(e[sl]).max() for e in err.values())
        for k, m in enumerate(["harmonic", "tv_converged"]):
            a = fig.add_subplot(sub[r, k])
            im = a.imshow(err[m][sl], cmap=div, vmin=-lim, vmax=lim, interpolation="nearest")
            a.set_xticks([]); a.set_yticks([]); a.grid(False)
            a.set_xlabel(f"{'Harmonic' if m == 'harmonic' else 'TV converged'}: RMSE {rm(m, b):.2f}", fontsize=8,
                         color=MUTED)
            if k == 0:
                a.set_title(tag, fontsize=7.5, loc="left")
        cax = fig.add_subplot(sub[r, 2])
        fig.colorbar(im, cax=cax)
        cax.tick_params(labelsize=7)
    axs[0, 0] = None
    fig.text(0.05, 0.955, f"(a) Signed error (grey levels) in 64x64 holes, smooth image; TV converged beats harmonic in "
             f"{wins} of {nb} blocks", fontsize=9, ha="left")
    # (b),(c) edge and texture retention, blocks32
    for a, q, t in [(axs[0, 1], "edge_retention", "(b) Edge-band gradient retention in the hole, blocks32"),
                    (axs[1, 0], "hf_retention", "(c) Laplacian (texture) energy retention in the hole, blocks32")]:
        w = 0.2
        real = [i for i in IMAGES if i != "smooth"]
        for j, m in enumerate(["harmonic", "biharmonic", "tv_shipped", "tv_converged"]):
            vals = [np.mean([r[q] for r in R if r["image"] == im and r["mask"] == "blocks32" and r["method"] == m])
                    for im in real]
            a.bar(np.arange(4) + (j - 1.5) * w, vals, w * 0.92, color=COL[m], label=LAB[m])
        a.set_xticks(range(4)); a.set_xticklabels(real); a.set_title(t + "\n(smooth image excluded: no edges, near-zero Laplacian)", fontsize=9)
        a.set_ylabel("reconstruction / truth (1 = preserved)")
    axs[0, 1].set_ylim(0, 0.34)
    axs[0, 1].legend(frameon=False, fontsize=7.5, ncol=2, loc="upper right")
    # (d) RMSE by distance, blocks64, mean over images and seeds
    a = axs[1, 1]
    for m in ["harmonic", "biharmonic", "tv_shipped", "tv_converged"]:
        agg = defaultdict(list)
        for d in D:
            if d["mask"] == "blocks64" and d["method"] == m:
                agg[(d["bin_lo"], d["bin_hi"])].append(d["rmse"])
        bins = sorted(agg)
        a.plot([min(b[1], 40) for b in bins], [np.mean(agg[b]) for b in bins], color=COL[m], marker=MARK[m], ms=4.5,
               lw=1.4, label=LAB[m])
    a.set_xscale("log"); a.set_xlabel("distance to nearest known pixel, bin upper edge (px)")
    a.set_ylabel("hole RMSE (grey levels)")
    a.set_title("(d) Error growth with distance from data, blocks64 (all images)", fontsize=9.5)
    fig.subplots_adjust(top=0.9, hspace=0.45, wspace=0.42)
    fig.savefig(os.path.join(FIG, "fig_failure_modes.png"), dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--recon-dir", required=True)
    a = ap.parse_args()
    os.makedirs(FIG, exist_ok=True)
    fig_comparison(a.recon_dir)
    fig_psnr_vs_inradius()
    fig_sensitivity()
    fig_convergence()
    fig_failure_modes(a.recon_dir)
    print("figures written to", FIG)
