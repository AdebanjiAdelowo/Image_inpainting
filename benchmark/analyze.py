"""Aggregate the benchmark CSVs into summary tables (markdown + CSV). No pandas needed."""
import csv
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402

from tvinpaint import data, metrics  # noqa: E402

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
METHODS = ["damaged", "meanfill", "harmonic", "biharmonic", "tv_shipped", "tv_corrected", "tv_converged"]
IMAGES = ["phantom", "camera", "astronaut", "grass", "smooth"]


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


def maxdist_by_mask():
    out = {}
    for kind in ["canonical", "dropout", "scratch", "blocks8", "blocks16", "blocks32", "blocks64"]:
        vals = [ndimage.distance_transform_edt(data.make_mask(kind, data.SHAPE, s)).max()
                for s in ([0] if kind == "canonical" else [0, 1, 2])]
        out[kind] = float(np.mean(vals))
    return out


def md_table(header, rows, fmt="{:.2f}"):
    def c(x):
        return fmt.format(x) if isinstance(x, (float, np.floating)) else str(x)
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    lines += ["| " + " | ".join(c(x) for x in r) + " |" for r in rows]
    return "\n".join(lines)


def main():
    R = load("benchmark_results.csv")
    T = load("convergence_trace.csv")
    D = load("error_by_distance.csv")
    md = defaultdict(list)
    md_out = []
    maxd = maxdist_by_mask()
    order = sorted(maxd, key=lambda k: maxd[k])
    md_out.append("## Mask geometry (area matched at about 16.2 %)\n")
    md_out.append(md_table(["mask", "mean max distance to known px (inradius)"], [[k, maxd[k]] for k in order], "{:.1f}"))

    # index
    idx = defaultdict(dict)
    for r in R:
        idx[(r["image"], r["mask"], int(r["seed"]))][r["method"]] = r
    cases = sorted(idx)

    # --- Table A: PSNR_hole per image x mask (mean +- sd over seeds)
    for metric, label in [("psnr_hole", "PSNR on hole pixels (dB)"), ("ssim_hole", "SSIM over hole pixels")]:
        md_out.append(f"\n## {label}, mean over seeds (canonical mask: single case)\n")
        summ = []
        for im in IMAGES:
            rows = []
            for k in order:
                vals = {m: [idx[c][m][metric] for c in cases if c[0] == im and c[1] == k] for m in METHODS}
                rows.append([k] + [np.mean(vals[m]) for m in METHODS])
                for m in METHODS:
                    summ.append(dict(image=im, mask=k, method=m, metric=metric, mean=np.mean(vals[m]),
                                     sd=np.std(vals[m]), n=len(vals[m])))
            md_out.append(f"\n**{im}**\n")
            md_out.append(md_table(["mask"] + METHODS, rows, "{:.2f}" if metric == "psnr_hole" else "{:.3f}"))
        with open(os.path.join(RES, f"summary_{metric}.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, lineterminator="\n", fieldnames=list(summ[0]))
            w.writeheader()
            w.writerows(summ)

    # --- Table B: paired comparison against the simple baselines
    md_out.append("\n## Paired differences in hole PSNR (dB), all cases\n")
    pairs = [("tv_shipped", "harmonic"), ("tv_converged", "harmonic"), ("tv_shipped", "biharmonic"),
             ("tv_converged", "biharmonic"), ("harmonic", "biharmonic"), ("tv_converged", "tv_shipped")]
    rows = []
    for a, b in pairs:
        d = np.array([idx[c][a]["psnr_hole"] - idx[c][b]["psnr_hole"] for c in cases])
        rows.append([f"{a} - {b}", d.mean(), np.median(d), d.min(), d.max(), f"{(d > 0).sum()}/{len(d)}"])
    md_out.append(md_table(["pair", "mean", "median", "min", "max", "TV-side wins"], rows))
    md_out.append("\n### by mask kind (mean over images and seeds): tv_converged - harmonic, tv_shipped - harmonic\n")
    rows = []
    for k in order:
        cs = [c for c in cases if c[1] == k]
        dc = np.mean([idx[c]["tv_converged"]["psnr_hole"] - idx[c]["harmonic"]["psnr_hole"] for c in cs])
        ds = np.mean([idx[c]["tv_shipped"]["psnr_hole"] - idx[c]["harmonic"]["psnr_hole"] for c in cs])
        wins = sum(idx[c]["tv_converged"]["psnr_hole"] > idx[c]["harmonic"]["psnr_hole"] for c in cs)
        rows.append([k, maxd[k], ds, dc, f"{wins}/{len(cs)}"])
    md_out.append(md_table(["mask", "inradius", "shipped - harmonic", "converged - harmonic", "converged wins"], rows))
    md_out.append("\n### by image (mean over masks and seeds)\n")
    rows = []
    for im in IMAGES:
        cs = [c for c in cases if c[0] == im]
        rows.append([im] + [np.mean([idx[c][a]["psnr_hole"] - idx[c][b]["psnr_hole"] for c in cs])
                            for a, b in [("tv_shipped", "harmonic"), ("tv_converged", "harmonic"),
                                         ("tv_converged", "biharmonic")]] +
                    [sum(idx[c]["tv_converged"]["psnr_hole"] > idx[c]["harmonic"]["psnr_hole"] for c in cs), len(cs)])
    md_out.append(md_table(["image", "shipped - harmonic", "converged - harmonic", "converged - biharmonic",
                            "converged wins vs harmonic", "cases"], rows))

    # --- Improvement over 'no restoration' and mean fill
    md_out.append("\n## Improvement of shipped TV over no restoration / mean fill (hole PSNR, dB; mean of all cases)\n")
    md_out.append(md_table(["comparison", "mean dB gain"], [
        ["tv_shipped - damaged", np.mean([idx[c]["tv_shipped"]["psnr_hole"] - idx[c]["damaged"]["psnr_hole"] for c in cases])],
        ["tv_shipped - meanfill", np.mean([idx[c]["tv_shipped"]["psnr_hole"] - idx[c]["meanfill"]["psnr_hole"] for c in cases])]]))

    # --- Documented defects: do they change the quantitative results?
    md_out.append("\n## Effect of the documented implementation defects (hole PSNR, dB)\n")
    rows = []
    for a, b, lab in [("tv_shipped_feasible", "tv_shipped", "return u_test instead of u (forward sweep)"),
                      ("tv_corrected", "tv_shipped_feasible", "symmetric R-B-R sweep instead of R-B (both u_test)"),
                      ("tv_corrected", "tv_shipped", "both corrections")]:
        d = np.array([idx[c][a]["psnr_hole"] - idx[c][b]["psnr_hole"] for c in cases])
        rows.append([lab, d.mean(), np.abs(d).max(), d.min(), d.max()])
    md_out.append(md_table(["change", "mean", "max abs", "min", "max"], rows, "{:.3f}"))
    kv = np.array([idx[c]["tv_shipped"]["known_violation"] for c in cases])
    md_out.append(f"\nShipped iterate `u`: max |u - f| on known pixels over all cases: median {np.median(kv):.2f}, "
                  f"max {kv.max():.2f} grey levels; `u_test` violation max "
                  f"{max(idx[c]['tv_shipped_feasible']['known_violation'] for c in cases):.1e}.")

    # --- Metric sanity: clipping and range
    gap = np.array([abs(idx[c][m]["rmse_hole"] - idx[c][m]["rmse_hole_unclipped"]) / idx[c][m]["rmse_hole"]
                    for c in cases for m in METHODS])
    oor = np.array([idx[c]["tv_shipped"]["out_of_range_frac_hole"] for c in cases])
    md_out.append(f"\n## Metric sanity\n\nRelative hole-RMSE change caused by clipping to [0,255]: max {gap.max():.2e}, "
                  f"median {np.median(gap):.2e}. Fraction of hole pixels outside [0,255] for `tv_shipped`: "
                  f"max {oor.max():.3f}, mean {oor.mean():.4f}.")

    # --- Convergence
    md_out.append("\n## Convergence of the shipped setting (200 iterations) relative to the 1500-iteration reference\n")
    tr = defaultdict(dict)
    for t in T:
        tr[(t["image"], t["mask"], int(t["seed"]))][int(t["k"])] = t
    rows = []
    for k in order:
        cs = [c for c in tr if c[1] == k]
        rd = np.median([tr[c][200]["rel_dist_to_ref"] for c in cs])
        eg = np.median([(tr[c][200]["tv_energy"] - tr[c][1500]["tv_energy"]) / tr[c][1500]["tv_energy"] for c in cs])
        dp = np.mean([tr[c][200]["psnr_hole"] - tr[c][1500]["psnr_hole"] for c in cs])
        best = np.mean([max(tr[c][kk]["psnr_hole"] for kk in tr[c]) - tr[c][1500]["psnr_hole"] for c in cs])
        rows.append([k, maxd[k], rd, eg, dp, best])
    md_out.append(md_table(["mask", "inradius", "median rel dist to ref @200", "median TV excess @200",
                            "mean dPSNR(200 - 1500)", "mean gain of best checkpoint over 1500"], rows, "{:.4g}"))
    md_out.append("\n### rel distance to reference and hole PSNR by iteration (median/mean over all cases)\n")
    ks = sorted({int(t["k"]) for t in T})
    rows = [[k, np.median([tr[c][k]["rel_dist_to_ref"] for c in tr]), np.mean([tr[c][k]["psnr_hole"] for c in tr]),
             np.median([tr[c][k]["rel_change"] for c in tr])] for k in ks]
    md_out.append(md_table(["k", "median rel dist to ref", "mean hole PSNR", "median rel change of u"], rows, "{:.4g}"))
    best_k = defaultdict(int)
    for c in tr:
        best_k[max(tr[c], key=lambda kk: tr[c][kk]["psnr_hole"])] += 1
    md_out.append("\nCheckpoint with the highest hole PSNR, count of cases: " +
                  ", ".join(f"k={k}: {best_k[k]}" for k in sorted(best_k)))

    # --- Failure-mode diagnostics
    md_out.append("\n## Failure-mode diagnostics inside the hole (mean over seeds)\n")
    diag = ["edge_retention", "hf_retention", "jump_conc", "flat_frac", "grad_ratio"]
    truth = data.evaluation_images()
    for k in ["blocks32", "blocks64", "canonical"]:
        md_out.append(f"\n**mask {k}**  (truth row: diagnostics of the true image over the same hole)\n")
        rows = []
        for im in IMAGES:
            seeds = [0] if k == "canonical" else [0, 1, 2]
            t_d = [metrics.hole_diagnostics(truth[im], truth[im], data.make_mask(k, data.SHAPE, s)) for s in seeds]
            rows.append([im, "truth"] + [np.mean([d[q] for d in t_d]) for q in diag])
            for m in ["harmonic", "biharmonic", "tv_shipped", "tv_converged"]:
                rows.append([im, m] + [np.mean([idx[(im, k, s)][m][q] for s in seeds]) for q in diag])
        md_out.append(md_table(["image", "method"] + diag, rows, "{:.3f}"))

    # --- error by distance
    md_out.append("\n## Hole RMSE by distance to the nearest known pixel (mean over images and seeds)\n")
    for k in ["canonical", "blocks32", "blocks64"]:
        agg = defaultdict(list)
        for d in D:
            if d["mask"] == k:
                agg[(d["method"], d["bin_lo"], d["bin_hi"])].append(d["rmse"])
        bins = sorted({(b[1], b[2]) for b in agg})
        ms = ["harmonic", "biharmonic", "tv_shipped", "tv_converged"]
        rows = [[f"({lo:g}, {min(hi, 99):g}]"] + [np.mean(agg[(m, lo, hi)]) if agg[(m, lo, hi)] else float("nan")
                                                  for m in ms] for lo, hi in bins]
        md_out.append(f"\n**mask {k}**\n")
        md_out.append(md_table(["distance (px)"] + ms, rows))

    # --- runtime
    md_out.append("\n## Runtime (parallel run on a loaded machine; see serial timing for clean numbers)\n")
    rows = []
    for m in METHODS[2:]:
        v = np.array([idx[c][m]["runtime_s"] for c in cases])
        rows.append([m, np.median(v), np.percentile(v, 10), np.percentile(v, 90)])
    md_out.append(md_table(["method", "median s", "p10", "p90"], rows))

    # --- sensitivity + noise, if present
    sp = os.path.join(RES, "sensitivity_dev.csv")
    if os.path.exists(sp):
        S = load("sensitivity_dev.csv")
        md_out.append("\n## Parameter sensitivity on held-out development images\n")
        for exp in sorted({s["experiment"] for s in S}):
            md_out.append(f"\n**{exp}**\n")
            sub = [s for s in S if s["experiment"] == exp]
            cols = ["case", "value", "rmse_hole_u", "rmse_hole_utest", "tv_utest", "hole_mean_u", "truth_hole_mean",
                    "finite", "runtime_s"] + (["rel_dist_to_2000"] if exp == "S3_iterations" else [])
            md_out.append(md_table(cols, [[s.get(c, "") for c in cols] for s in sub], "{:.4g}"))
    npath = os.path.join(RES, "noise_known_pixels.csv")
    if os.path.exists(npath):
        N = load("noise_known_pixels.csv")
        md_out.append("\n## Noise on the known pixels (canonical mask, shipped TV), mean over noise seeds\n")
        rows = []
        for im in sorted({n["image"] for n in N}):
            for s in sorted({n["noise_sigma"] for n in N}):
                row = [im, s]
                for m in ["noisy_observation", "harmonic", "biharmonic", "tv_shipped"]:
                    v = [n for n in N if n["image"] == im and n["noise_sigma"] == s and n["method"] == m]
                    row += [np.mean([x["psnr_hole"] for x in v]), np.mean([x["psnr_full"] for x in v])]
                rows.append(row)
        md_out.append(md_table(["image", "noise sd", "noisy obs hole", "full", "harmonic hole", "full",
                                "biharmonic hole", "full", "tv_shipped hole", "full"], rows))
    open(os.path.join(RES, "tables.md"), "w").write("\n".join(md_out) + "\n")
    print("wrote tables.md")


if __name__ == "__main__":
    main()
