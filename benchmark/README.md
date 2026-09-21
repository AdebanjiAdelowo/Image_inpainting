# Quantitative benchmark and limitation analysis

This directory measures how well the repository's TV-inpainting solver actually reconstructs
images, against known ground truth, and compares it with simpler methods that use the identical
damaged input. It runs the verified `tvinpaint` solver; the historical notebook algorithm is
available as `legacy=True` (bit-identical to the notebooks, verified by `tests/test_solver.py`) and is
benchmarked alongside it so the effect of each correction is measured, not assumed.

## What is being solved (and what is not)

The model is **hard-constrained, noise-free inpainting**:

    min_u  sum_ij |(grad u)_ij|_2      subject to   u = f on the known pixels

with forward-difference gradient (zero in the last row/column), isotropic TV, and the
Bredies-Sun preconditioned Douglas-Rachford iteration. There is **no regularisation weight
lambda** (the minimiser is independent of the dual-ball radius) and **no noise model**, so
"sweep lambda" and "noise level" do not exist for this model. The difficulty axis is the geometry
of the damage. The repository's canonical experiment (`u0.png`, `lossregion.png`) has no clean
image, so it cannot be scored with PSNR/SSIM; the benchmark therefore transplants the repository's
own loss mask, and synthetic masks of the same area, onto standard images with known truth.

## Protocol (frozen before any evaluation result was seen)

* Solver settings are exactly the historical ones: sigma = 14, tau = 1/14, 3 inner sweeps,
  200 iterations, warm start from the damaged image (hole = 255). Nothing is tuned on the
  evaluation set.
* Images (436 x 455, float in [0, 255]): `phantom` (Shepp-Logan, piecewise constant), `camera`
  (edges plus texture), `astronaut` (grey, natural), `grass` (texture), `smooth` (synthetic,
  edge-free). All are bundled with scikit-image or generated deterministically.
* Masks (all about 16.2 % of the pixels, so only the hole geometry changes): the canonical mask;
  random pixel dropout; random thin scratches; random non-overlapping square blocks of side
  8, 16, 32, 64. Three seeds per random family; 95 cases in total.
* Methods, all given the same damaged input and known set: no restoration (`damaged`), mean fill,
  harmonic (exact solve of min sum |grad u|^2 s.t. the same constraint, the quadratic counterpart of
  the TV problem), biharmonic (scikit-image reference), and four TV variants:

  | column `method` | how it is produced |
  |---|---|
  | `tv_shipped` | historical notebook algorithm, `pdr_inpaint(..., legacy=True).u_dr`, 200 iterations |
  | `tv_shipped_feasible` | the same run's feasible iterate, `pdr_inpaint(..., legacy=True).u` |
  | `tv_corrected` | verified default solver, `pdr_inpaint(...).u`, 200 iterations |
  | `tv_converged` | verified default solver, 1500 iterations (separates solver error from model error) |
* Metrics: PSNR (data range 255, float, no quantisation) and SSIM on the reconstruction clipped to
  [0, 255]. The headline metric is **PSNR on the hole pixels only**, because the known pixels are
  constrained and inflate whole-image numbers.
* Parameter sensitivity (`run_sensitivity.py`) uses held-out development images (`moon`, `coins`),
  never the evaluation images, and selects nothing.

## Reproduce

```bash
python -m pytest tests -q                                    # 47 tests, about 5 s
python benchmark/reproduce_canonical.py                      # canonical run, serial timing
python benchmark/run_benchmark.py --recon-dir /tmp/recons    # about 25 min, 4 workers
python benchmark/run_sensitivity.py                          # held-out development set
python benchmark/run_noise.py                                # noisy known pixels (scope check)
python benchmark/run_init_check.py                           # warm-start check of the converged reference
python benchmark/analyze.py                                  # results/tables.md
python benchmark/make_figures.py --recon-dir /tmp/recons     # figures/
```

Requirements: `numpy`, `scipy`, `scikit-image`, `Pillow`, `matplotlib`, `pytest`. Machine-readable results are in `results/`; `run_metadata.json` records
versions, configuration, repository HEAD and machine load.

## Findings (details and all tables in `results/tables.md`)

1. **The canonical run reproduces exactly** with `legacy=True` (TV energy 1,408,290; max constraint
   violation 1.45 grey levels), and the verified solver returns a solution that satisfies the constraint
   exactly (energy 1,407,541; the two outputs differ by 2.4 % relative L2 in the hole, mostly from the
   sweep change). See `results/canonical_reproduction.json` for runtimes, hole statistics and the
   decomposition of the difference.
2. **TV is a large improvement over doing nothing**, and beats mean fill by a mean of 13.6 dB hole
   PSNR, but that is a low bar.
3. **TV does not beat the quadratic baselines in general.** On the four images with real content,
   converged TV differs from harmonic inpainting by 0.00 dB on average (median -0.26 dB; TV wins
   28 of 76 cases) and from biharmonic by -0.14 dB (31 of 76). On the edge-free `smooth` image TV
   is 4.9 dB worse than harmonic and far worse than biharmonic (it never wins).
4. **Where TV does win**: piecewise-constant content with thin damage. On the phantom, converged
   TV beats harmonic by 2.9 dB (pixel dropout), 4.0 dB (scratches) and 2.1 dB (canonical mask), and
   biharmonic by 1.0, 2.0 and 0.9 dB. The same phantom with 16-32 px blocks is 1.1-1.3 dB worse
   than harmonic.
5. **Hole geometry, not area, governs quality.** At a fixed 16.2 % damaged area, hole PSNR falls
   by 6 to 18 dB from pixel dropout to 64 px blocks on the four real-content images, for every
   method (grass 6 dB for harmonic and TV, phantom 18 dB for TV).
6. **200 iterations are not converged for large holes.** Compared with 1500 iterations the verified
   solver loses on average 0.6 dB (16 px inradius), 2.3 dB (canonical mask, 18 px) and 6.6 dB (32 px);
   the historical solver loses 1.0, 2.2 and 7.2 dB. On the darker phantom with the canonical mask the
   historical loss is 7.4 dB. Reconstruction error is not
   monotone in the iteration count: in 75 of 95 cases the best checkpoint is earlier than 1500
   iterations, although the mean gain from stopping there is under 0.25 dB (larger on some
   development images, e.g. RMSE 40.4 at k=300 vs 47.1 converged on `coins`).
7. **Measured failure modes.** Texture: converged TV keeps 3-17 % of the true Laplacian energy in
   the hole (grass 3 %) and fills 64 px holes on `grass` with a flat patch. Staircasing on the
   edge-free image (seed 0, 64 px blocks): per-block RMSE of converged TV ranges from 0.4 to 7.8 grey
   levels, against 1.0 to 3.9 for harmonic and at most 0.31 for biharmonic; TV beats harmonic in only
   2 of the 8 blocks, and the error is a flat plateau rather than noise. Edge retention (a
   magnitude index, not a position check): for holes of 32 px and larger converged TV keeps no more
   of the edge-band gradient than harmonic (0.184 vs 0.185 on the phantom, blocks32); its advantage
   appears only with thin damage on the phantom (0.72 vs 0.55 with the canonical mask), and not on
   the natural images (camera 0.23 vs 0.24).
8. **The corrected defects** (forward-only sweep, raw iterate instead of the feasible one) change hole
   PSNR by at most 0.22 dB (returned iterate) and 1.8 dB (sweep, at 200 iterations); the verified default
   differs from the historical solver by +0.15 dB on average (range -2.0 to +1.5 dB, and -0.06 to +1.07 dB
   on the real-content images) and does not alter any conclusion. The lambda/mu inner-solver defect is
   inert at sigma*tau = 1, so no historical or benchmark result is affected by it, but it is real away
   from that case: the historical solver diverges or overflows (`results/sensitivity_dev.csv`, S4), the
   corrected one does not (`tests/test_solver.py`, analytic regression test).
9. **Noise on the known pixels** (`results/noise_known_pixels.csv`): the hard constraint copies
   the noise, so whole-image PSNR is bounded by the noise level; hole PSNR
   degrades by about 1 dB at noise sd 30 on the three real-content images for TV and harmonic,
   against about 3.6 dB for biharmonic on the camera image. On `smooth`, TV is 0.5 dB (sd 15) and
   1.7 dB (sd 30) better than harmonic.

## Limitations of this benchmark

* Five images, one grey-scale resolution, area-matched masks with three seeds: it supports the
  regime statements above, not universal rankings.
* "Converged" means 1500 iterations; against 1000 iterations the hole PSNR moves by at most
  0.20 dB (mean 0.017 dB). The TV minimiser is not unique; a harmonic instead of white warm start
  changes the converged hole PSNR by at most 0.16 dB on the 10 cases checked
  (`results/init_check_converged.csv`).
* SSIM whole-image values are dominated by the known pixels; use the hole-restricted numbers.
* Edge, texture and staircasing indices are magnitude-based summaries; they do not check that an
  edge is in the right place. The ratio-type texture index is meaningless for the `smooth` image
  (near-zero Laplacian in the truth) and is excluded from the figures.
* Runtimes in `benchmark_results.csv` come from a parallel run on a busy machine; the clean serial
  timing is `results/canonical_reproduction.json`.
* The result files were generated on 2026-09-21 before the solver API was refactored (defaults changed to
  the verified variant, `legacy=True` added). The refactor was checked by re-running four complete cases
  (776 numbers: all methods, metrics and convergence traces) and by re-running the sensitivity, noise
  and warm-start scripts in full; every value is bit-identical to the stored files.
* The penalised (noise-aware) variant of the model is not implemented; a real lambda study needs it.
