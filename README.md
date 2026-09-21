# TV Inpainting via Preconditioned Douglas-Rachford Iteration

Total variation (TV) inpainting of missing image regions, solved with the Preconditioned
Douglas-Rachford splitting of Bredies and Sun. Pure NumPy: no deep learning, no external ML libraries.

The repository contains a **verified implementation** (the `tvinpaint` package, with tests and a
quantitative benchmark against known ground truth) and the **historical notebooks** it grew out of,
kept for provenance. Start with the package.

---

## Problem

Given a damaged image $f$ whose pixels in a loss region $\Omega''$ are missing, reconstruct $u$ by solving

$$\min_{u} \|\nabla u\|_{2,1} \quad \text{subject to} \quad u = f \text{ on } \Omega' = \Omega \setminus \Omega'',$$

with the forward-difference gradient (zero in the last row and column) and the isotropic discrete TV
$\|p\|_{2,1}=\sum_{ij}\sqrt{(p^y_{ij})^2+(p^x_{ij})^2}$.

This is **hard-constrained, noise-free inpainting**. The known pixels are treated as exact, so the model
has **no regularisation weight $\lambda$** (the minimiser does not depend on the TV weight) and **no
noise model**. A penalised, noise-aware TV restoration model, `alpha TV(u) + 1/2 ||u - f||^2` on the
known set, would be a separate extension and is not implemented here. The benchmark below therefore
varies the geometry of the damage and the solver budget, not a regularisation parameter.

## Quick start (verified implementation)

```bash
pip install numpy scipy scikit-image Pillow matplotlib pytest
python -m tvinpaint                       # inpaints u0.png with lossregion.png -> reconstruction.png
python -m tvinpaint --iters 1500          # more iterations for large holes (see Convergence)
python -m pytest tests -q                 # 47 tests
```

```python
from tvinpaint import pdr_inpaint

res = pdr_inpaint(f, known, iters=200)    # f: 2-D float image, known: boolean mask (True = data)
u = res.u                                 # the solution; u == f on the known pixels exactly
```

`res.u` is the feasible Douglas-Rachford iterate `u_test = P_C(2u - u_bar)`. It equals `f` on the
known pixels bit for bit, and converges to the same limit as the raw iterate (Bredies and Sun,
Remark 2.4). The raw iterate is available as `res.u_dr`.

## Implementation status: verified package versus historical notebooks

| | Historical notebooks (`legacy=True`) | Verified `tvinpaint` (default) |
|---|---|---|
| Inner solver | Forward red-black Gauss-Seidel sweep (red, then black) | Symmetric sweep (red, black, red) |
| Gauss-Seidel neighbour weight | `lamda` | `mu` |
| Returned iterate | Raw DR iterate `u`, satisfies $u=f$ only in the limit | Feasible iterate, satisfies $u=f$ exactly |

* **Forward versus symmetric.** The notebook function is named `sym_red_black_gauss_seidel` but performs
  a forward sweep, which gives a preconditioner that is not self-adjoint, so the convergence theorem does
  not apply to it verbatim. A symmetric sweep is red, black, red. The verified solver uses that; the
  historical behaviour is kept and correctly labelled as forward. (Verified numerically, see
  `tests/test_operators_and_prox.py` and docs Section 7.6.3.)
* **The `lamda`/`mu` defect.** The system is $(\lambda I-\mu\Delta)u=b$, so the Gauss-Seidel update
  is $u\leftarrow (b+\mu\sum u_{\text{nbr}})/(\lambda+k\mu)$. The notebooks weight the neighbour sum by
  `lamda`. The two coincide when $\sigma\tau=1$ ($\lambda=\mu=1$), which is the configuration of every
  result reported for the notebooks ($\sigma=14$, $\tau=1/14$), so **the historical canonical result was not affected**.
  For any other step size the historical expression solves a different system and the iteration
  diverges or overflows. The analytic regression test (`test_regression_mu_weighted_update_is_needed_away_from_sigma_tau_one`)
  reaches the exact optimum for $\sigma\tau\in\{0.5,2,4\}$ with the corrected update and fails with the old one.
* **Exact hard constraint.** The returned solution satisfies $u=f$ on the known pixels with zero
  deviation (tested for 1, 40 and 400 iterations, both modes). The raw iterate deviates by 1.45 grey
  levels on the canonical case after 200 iterations.
* **Reproducing the original result.** `pdr_inpaint(f, known, legacy=True).u_dr` (or
  `python -m tvinpaint --legacy`) is bit-identical to the notebooks; a test executes the notebook's own
  function cells and compares.

The historical canonical result is therefore **not invalidated** by these defects: at $\sigma\tau=1$ the
two neighbour-weight expressions coincide, and the constraint and sweep differences are quantified in the
canonical-case table below. The verified solver is nevertheless the current implementation because it is
correct away from that special case, uses the intended symmetric sweep, and returns an exactly feasible
iterate.

The notebooks ([`Image_Inpainting.ipynb`](Image_Inpainting.ipynb),
[`Adebanji_Image_Inpainting.ipynb`](Adebanji_Image_Inpainting.ipynb)) are unchanged except for a status
banner cell at the top. The technical documentation in `docs/` describes the historical implementation
and already records these defects (Sections 7.6.3, 8.7 and 9.8); its text and PDF are not updated.

### The canonical case, historical versus verified (200 iterations)

`u0.png` + `lossregion.png`, 436 x 455, 32,202 unknown pixels, sigma = 14, tau = 1/14, 3 sweeps,
warm start from `u0.png`. The canonical image has no clean original, so PSNR/SSIM cannot be computed on
it; the benchmark below transplants its loss mask onto images with known truth.

| | Historical (`u_dr`) | Verified (`u`) |
|---|---:|---:|
| TV energy | 1,408,290 | 1,407,541 |
| max abs deviation from $f$ on known pixels | 1.45 | 0 |
| mean of the reconstruction in the hole | 74.34 | 73.77 |
| relative distance to the 2000-iteration verified limit | 6.07e-2 | 5.30e-2 |
| runtime, single thread, Apple M3 Pro (machine load 3 to 5) | 2.3 to 3.3 s | 3.5 to 4.2 s |

The two outputs differ by 0.98 % (relative L2, whole image) and 2.4 % (hole only); 15 % of the hole
pixels differ by more than one grey level, at most by 15.5. About 90 % of that is the sweep change; the
constraint fix alone changes the hole by 0.19 % (at most 1.2 grey levels). The verified solver is
slightly closer to the limit at the same iteration count and 30 to 50 % slower per iteration (three
half-sweeps instead of two; the range reflects machine load).

## Algorithm

The TV minimisation is written as the saddle-point problem $\min_u\max_p \langle\nabla u,p\rangle + G(u) - F^*(p)$,
with $G$ the indicator of the data constraint and $F^*$ the indicator of the pointwise 2-norm ball, and
solved with the preconditioned Douglas-Rachford algorithm of

> *Preconditioned Douglas-Rachford Splitting Methods for Convex-Concave Saddle-Point Problems*
> Kristian Bredies, Hongpeng Sun, [SFB Report 2014-002](https://imsc.uni-graz.at/mobis/publications/SFB-Report-2014-002_2.pdf), 2014
> (SIAM J. Numer. Anal. 53(1), 2015)

Each iteration performs a preconditioned primal step (the linear system $(I-\mu\Delta)u=b$ solved
inexactly by red-black Gauss-Seidel), an exact dual update, and one reflection through each of the two
projections (onto the data set and onto the dual ball). The step parameters enter only through
$\sigma\tau$ (the linear system) and the dual-ball radius $\alpha/\tau$; the minimiser does not depend
on either, so they act as convergence-speed parameters.

## Benchmark against known ground truth

Details, all tables and machine-readable results are in [`benchmark/`](benchmark/README.md).

* **Protocol.** Five 436 x 455 images (Shepp-Logan phantom, `camera`, grey `astronaut`, `grass` texture, an
  edge-free synthetic `smooth` image) times 19 masks of equal area (16.2 %): the repository's canonical
  mask, random pixel dropout, thin scratches, and non-overlapping square blocks of side 8, 16, 32 and 64,
  three seeds each. 95 cases. Solver settings were fixed before any result was seen; nothing was tuned on
  the evaluation images (sensitivity studies use separate held-out images).
* **Baselines**, all given the identical damaged input: no restoration, mean fill, **harmonic**
  inpainting (the exact quadratic counterpart, $\min\sum|\nabla u|^2$ under the same constraint and
  gradient), and biharmonic inpainting (scikit-image).
* **Metric.** PSNR on the hole pixels only (range 255), because the constrained known pixels inflate
  whole-image numbers.

Mean hole PSNR (dB) over the four real-content images (phantom, camera, astronaut, grass) and seeds:

| mask | max distance to known pixel | harmonic | biharmonic | TV historical, 200 it | TV verified, 200 it | TV verified, 1500 it |
|---|---:|---:|---:|---:|---:|---:|
| pixel dropout | 1.6 px | 28.10 | 29.15 | 29.17 | 29.17 | 29.17 |
| blocks 8 | 4 px | 21.70 | 22.33 | 21.73 | 21.72 | 21.60 |
| scratches | 5.9 px | 24.55 | 25.58 | 25.22 | 25.23 | 25.25 |
| blocks 16 | 8 px | 19.57 | 19.81 | 19.14 | 19.16 | 19.05 |
| blocks 32 | 16 px | 17.29 | 16.46 | 15.96 | 16.18 | 16.50 |
| canonical mask | 18.4 px | 20.88 | 20.91 | 18.30 | 18.68 | 20.78 |
| blocks 64 | 32 px | 16.39 | 15.13 | 10.42 | 10.86 | 16.05 |

### Findings

This is not a universal ranking of inpainting algorithms; it covers five images and these mask families.

**Across the tested real-content cases in this benchmark, converged TV and harmonic inpainting have
similar mean hole PSNR, with strongly regime-dependent results.** On the four real-content images,
converged TV differs from harmonic by 0.00 dB on average (median -0.26 dB; TV is better in 28 of 76
cases) and from biharmonic by -0.14 dB (31 of 76). At the default 200 iterations the verified solver is
0.95 dB below harmonic on average (22 of 76). The regimes behave differently:

* TV's clearest advantage is for thin damage in piecewise-constant content: on the phantom, converged TV
  beats harmonic by 2.9 dB (pixel dropout), 4.0 dB (scratches) and 2.1 dB (canonical mask), and
  biharmonic by 1.0, 2.0 and 0.9 dB.
* Wide holes reduce that advantage: on the same phantom, 16 to 32 px blocks are 1.1 to 1.3 dB worse than
  harmonic.
* Texture is flattened.
* Smooth content strongly favours the quadratic alternatives: on the edge-free image TV is 4.9 dB below
  harmonic and never beats either baseline.

Against doing nothing TV is a large gain (+22.7 dB over the damaged input and +13.6 dB over mean fill for
the historical solver, mean of all 95 cases), but that is a low bar.

* **Hole geometry, not area, governs quality.** At a fixed 16.2 % damaged area, hole PSNR falls by 6 to
  18 dB from pixel dropout to 64 px blocks on the four real-content images, for every method.
* **Convergence and budget.** The default 200 iterations are not converged for large holes. Compared
  with 1500 iterations, the verified solver loses on average 0.6 dB (16 px blocks), 2.3 dB (canonical
  mask) and 6.6 dB (64 px blocks); the historical solver loses 1.0, 2.2 and 7.2 dB. On the darker
  phantom with the canonical mask the historical loss is 7.4 dB. Below about 8 px inradius the loss is
  under 0.1 dB. Error is not monotone in the iteration count (in 75 of 95 cases the best checkpoint is
  earlier than 1500 iterations, by under 0.25 dB on average). Use `iters=1500` for holes above about
  15 px inradius; the default stays at 200 for continuity with the historical result. The 1500-iteration
  reference moves by at most 0.20 dB relative to 1000 iterations, and a harmonic warm start changes it
  by at most 0.16 dB, so "converged" is a reliable reference despite the non-uniqueness of TV minimisers.
* **Measured failure modes.**
  *Texture*: converged TV keeps 3 to 17 % of the true Laplacian energy in the hole (grass 3 %) and fills a
  64 px hole on `grass` with a flat patch.
  *Staircasing on smooth content*: on the edge-free image (seed 0, 64 px blocks) per-block RMSE is
  0.4 to 7.8 grey levels for converged TV against 1.0 to 3.9 for harmonic and at most 0.31 for biharmonic;
  TV is better than harmonic in only 2 of the 8 blocks, and the error is a flat plateau.
  *Edges*: for holes of 32 px and larger, converged TV keeps no more of the edge-band gradient than
  harmonic (0.184 versus 0.185 on the phantom); its advantage appears with thin damage on the phantom
  (0.72 versus 0.55) and not on the natural images (camera 0.23 versus 0.24). This is a magnitude index and
  does not check that an edge is in the right place.
  *Accuracy versus distance* (64 px blocks, mean over the five images): all methods degrade with distance
  from known data; converged TV is much worse than harmonic right next to the data (RMSE 27.8 versus 15.2
  grey levels in the first pixel) and comparable beyond about 8 px.
* **Noise on the known pixels** (a scope check, not a noise-aware model): the hard constraint copies the
  noise, so whole-image PSNR is capped by the noise level; hole PSNR drops by about 1 dB at noise sd 30 for
  TV and harmonic on the real-content images, against 3.6 dB for biharmonic on `camera`.
* **Do the corrections change the conclusions?** No. The verified default differs from the historical
  solver by +0.15 dB in mean hole PSNR (range -2.0 to +1.5 dB over 95 cases, and -0.06 to +1.07 dB on the
  real-content images); the constraint fix alone changes it by at most 0.22 dB.

### Limitations

* Five images, one resolution, area-matched masks with three seeds: this supports the regime statements
  above, not a general ranking. Whole-image SSIM is dominated by the known pixels; use the hole numbers.
* The edge, texture and staircasing indices are magnitude-based; the texture ratio is meaningless on the
  `smooth` image and is excluded from the figures.
* Runtimes in the benchmark CSV come from a busy machine; the clean serial timing is in
  `benchmark/results/canonical_reproduction.json`.
* No noise-aware model, no colour (vectorial TV), no multigrid or adaptive step size.
* The technical PDF in `docs/` was not regenerated and describes the historical implementation.

## Structure

```
Image_inpainting/
├── tvinpaint/                       # verified implementation (solver, operators, baselines, metrics, data)
│   └── __main__.py                  #   python -m tvinpaint
├── tests/                           # 47 tests: operators, prox, solver, baselines, metrics, CLI
├── benchmark/                       # protocol, scripts, results/*.csv|json, figures/, README.md
├── Image_Inpainting.ipynb           # historical notebook (banner added, code unchanged)
├── Adebanji_Image_Inpainting.ipynb  # historical development notebook (banner added, code unchanged)
├── docs/                            # technical documentation of the historical implementation
├── u0.png                           # damaged input image
└── lossregion.png                   # binary loss mask: black (0) = known, white (255) = unknown
```

To use your own image, pass `--image` and `--mask` to `python -m tvinpaint`
(mask: black = known, white = unknown), or call `pdr_inpaint` directly.
