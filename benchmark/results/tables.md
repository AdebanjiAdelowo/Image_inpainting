## Mask geometry (area matched at about 16.2 %)

| mask | mean max distance to known px (inradius) |
|---|---|
| dropout | 1.6 |
| blocks8 | 4.0 |
| scratch | 5.9 |
| blocks16 | 8.0 |
| blocks32 | 16.0 |
| canonical | 18.4 |
| blocks64 | 32.0 |

## PSNR on hole pixels (dB), mean over seeds (canonical mask: single case)


**phantom**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 0.90 | 13.61 | 30.92 | 32.82 | 33.81 | 33.81 | 33.79 |
| blocks8 | 1.05 | 12.78 | 22.07 | 24.07 | 23.48 | 23.45 | 23.01 |
| scratch | 0.98 | 13.65 | 26.75 | 28.75 | 30.65 | 30.67 | 30.75 |
| blocks16 | 1.05 | 12.93 | 19.37 | 21.43 | 18.92 | 18.92 | 18.24 |
| blocks32 | 1.07 | 13.07 | 16.67 | 16.83 | 14.46 | 14.90 | 15.40 |
| canonical | 0.83 | 14.46 | 23.49 | 24.69 | 18.18 | 19.25 | 25.59 |
| blocks64 | 1.14 | 13.73 | 15.77 | 15.20 | 6.82 | 7.29 | 15.47 |

**camera**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 4.49 | 10.61 | 29.27 | 29.83 | 29.87 | 29.87 | 29.87 |
| blocks8 | 4.43 | 10.63 | 23.49 | 23.66 | 22.86 | 22.85 | 22.85 |
| scratch | 4.23 | 10.85 | 25.85 | 26.43 | 25.60 | 25.60 | 25.60 |
| blocks16 | 4.31 | 10.58 | 21.67 | 21.44 | 21.36 | 21.39 | 21.55 |
| blocks32 | 4.29 | 10.64 | 19.27 | 17.27 | 18.36 | 18.56 | 19.10 |
| canonical | 4.01 | 10.33 | 20.95 | 20.33 | 19.69 | 19.91 | 20.49 |
| blocks64 | 3.69 | 9.97 | 18.01 | 17.57 | 10.32 | 10.78 | 18.11 |

**astronaut**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 4.14 | 10.71 | 29.65 | 31.12 | 30.38 | 30.38 | 30.38 |
| blocks8 | 4.12 | 10.72 | 22.79 | 23.61 | 22.84 | 22.84 | 22.83 |
| scratch | 3.93 | 10.70 | 25.57 | 26.95 | 25.29 | 25.29 | 25.28 |
| blocks16 | 4.02 | 10.55 | 19.84 | 20.16 | 19.52 | 19.56 | 19.62 |
| blocks32 | 4.18 | 10.40 | 16.43 | 17.31 | 14.67 | 14.88 | 15.14 |
| canonical | 3.90 | 10.71 | 20.82 | 21.96 | 17.69 | 17.87 | 19.35 |
| blocks64 | 3.97 | 10.39 | 15.29 | 14.33 | 10.03 | 10.38 | 14.27 |

**grass**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 5.07 | 16.35 | 22.54 | 22.83 | 22.62 | 22.62 | 22.62 |
| blocks8 | 5.03 | 16.38 | 18.46 | 17.99 | 17.73 | 17.73 | 17.73 |
| scratch | 5.08 | 16.34 | 20.02 | 20.18 | 19.35 | 19.35 | 19.35 |
| blocks16 | 5.02 | 16.35 | 17.39 | 16.22 | 16.77 | 16.77 | 16.78 |
| blocks32 | 5.11 | 16.32 | 16.77 | 14.42 | 16.35 | 16.36 | 16.36 |
| canonical | 5.02 | 16.18 | 18.27 | 16.67 | 17.66 | 17.68 | 17.71 |
| blocks64 | 5.08 | 16.35 | 16.49 | 13.42 | 14.52 | 14.97 | 16.34 |

**smooth**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 4.89 | 14.34 | 84.98 | 96.29 | 79.79 | 79.83 | 80.25 |
| blocks8 | 5.17 | 14.40 | 67.97 | 119.20 | 64.24 | 64.25 | 64.27 |
| scratch | 5.25 | 14.49 | 67.92 | 76.29 | 61.26 | 60.88 | 61.22 |
| blocks16 | 5.19 | 14.53 | 57.72 | 100.40 | 53.70 | 53.76 | 53.86 |
| blocks32 | 5.51 | 14.37 | 46.07 | 76.84 | 39.23 | 40.49 | 42.18 |
| canonical | 5.38 | 14.81 | 59.75 | 94.52 | 46.09 | 44.09 | 47.38 |
| blocks64 | 5.68 | 13.82 | 34.97 | 56.95 | 17.28 | 18.43 | 30.88 |

## SSIM over hole pixels, mean over seeds (canonical mask: single case)


**phantom**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 0.066 | 0.281 | 0.997 | 0.998 | 0.999 | 0.999 | 0.999 |
| blocks8 | 0.055 | 0.184 | 0.943 | 0.960 | 0.981 | 0.981 | 0.982 |
| scratch | 0.048 | 0.199 | 0.983 | 0.991 | 0.995 | 0.995 | 0.995 |
| blocks16 | 0.086 | 0.231 | 0.867 | 0.903 | 0.921 | 0.926 | 0.939 |
| blocks32 | 0.116 | 0.274 | 0.711 | 0.783 | 0.391 | 0.646 | 0.873 |
| canonical | 0.058 | 0.197 | 0.880 | 0.923 | 0.770 | 0.811 | 0.963 |
| blocks64 | 0.152 | 0.353 | 0.601 | 0.704 | 0.231 | 0.241 | 0.839 |

**camera**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 0.173 | 0.347 | 0.978 | 0.978 | 0.978 | 0.978 | 0.978 |
| blocks8 | 0.099 | 0.210 | 0.825 | 0.822 | 0.820 | 0.820 | 0.820 |
| scratch | 0.099 | 0.276 | 0.903 | 0.903 | 0.898 | 0.898 | 0.898 |
| blocks16 | 0.179 | 0.262 | 0.701 | 0.693 | 0.702 | 0.703 | 0.706 |
| blocks32 | 0.246 | 0.308 | 0.608 | 0.588 | 0.563 | 0.576 | 0.620 |
| canonical | 0.143 | 0.237 | 0.780 | 0.779 | 0.766 | 0.767 | 0.772 |
| blocks64 | 0.251 | 0.309 | 0.543 | 0.531 | 0.356 | 0.361 | 0.568 |

**astronaut**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 0.206 | 0.449 | 0.989 | 0.991 | 0.990 | 0.990 | 0.990 |
| blocks8 | 0.105 | 0.279 | 0.848 | 0.874 | 0.855 | 0.855 | 0.855 |
| scratch | 0.122 | 0.351 | 0.946 | 0.959 | 0.944 | 0.944 | 0.944 |
| blocks16 | 0.165 | 0.269 | 0.675 | 0.723 | 0.694 | 0.696 | 0.700 |
| blocks32 | 0.218 | 0.277 | 0.527 | 0.587 | 0.434 | 0.467 | 0.534 |
| canonical | 0.150 | 0.306 | 0.785 | 0.827 | 0.758 | 0.769 | 0.786 |
| blocks64 | 0.250 | 0.288 | 0.405 | 0.466 | 0.341 | 0.346 | 0.449 |

**grass**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 0.351 | 0.857 | 0.966 | 0.968 | 0.965 | 0.965 | 0.965 |
| blocks8 | 0.106 | 0.510 | 0.655 | 0.666 | 0.594 | 0.594 | 0.594 |
| scratch | 0.177 | 0.676 | 0.842 | 0.858 | 0.814 | 0.814 | 0.814 |
| blocks16 | 0.081 | 0.317 | 0.409 | 0.415 | 0.347 | 0.347 | 0.347 |
| blocks32 | 0.073 | 0.207 | 0.259 | 0.247 | 0.218 | 0.218 | 0.218 |
| canonical | 0.132 | 0.474 | 0.595 | 0.608 | 0.558 | 0.558 | 0.558 |
| blocks64 | 0.069 | 0.145 | 0.172 | 0.159 | 0.140 | 0.143 | 0.147 |

**smooth**

| mask | damaged | meanfill | harmonic | biharmonic | tv_shipped | tv_corrected | tv_converged |
|---|---|---|---|---|---|---|---|
| dropout | 0.046 | 0.367 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| blocks8 | 0.071 | 0.333 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| scratch | 0.031 | 0.309 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| blocks16 | 0.288 | 0.525 | 1.000 | 1.000 | 0.999 | 0.999 | 0.999 |
| blocks32 | 0.476 | 0.673 | 0.999 | 1.000 | 0.991 | 0.993 | 0.996 |
| canonical | 0.199 | 0.459 | 1.000 | 1.000 | 0.997 | 0.996 | 0.997 |
| blocks64 | 0.587 | 0.753 | 0.992 | 1.000 | 0.832 | 0.853 | 0.980 |

## Paired differences in hole PSNR (dB), all cases

| pair | mean | median | min | max | TV-side wins |
|---|---|---|---|---|---|
| tv_shipped - harmonic | -2.40 | -0.70 | -25.34 | 4.58 | 21/95 |
| tv_converged - harmonic | -0.98 | -0.41 | -12.36 | 5.11 | 28/95 |
| tv_shipped - biharmonic | -8.13 | -0.87 | -55.77 | 2.67 | 22/95 |
| tv_converged - biharmonic | -6.71 | -0.72 | -55.74 | 3.45 | 31/95 |
| harmonic - biharmonic | -5.73 | -0.53 | -51.96 | 3.64 | 29/95 |
| tv_converged - tv_shipped | 1.41 | 0.03 | -1.06 | 19.85 | 68/95 |

### by mask kind (mean over images and seeds): tv_converged - harmonic, tv_shipped - harmonic

| mask | inradius | shipped - harmonic | converged - harmonic | converged wins |
|---|---|---|---|---|
| dropout | 1.61 | -0.18 | -0.09 | 12/15 |
| blocks8 | 4.00 | -0.73 | -0.82 | 5/15 |
| scratch | 5.91 | -0.79 | -0.78 | 3/15 |
| blocks16 | 8.00 | -1.14 | -1.19 | 2/15 |
| blocks32 | 16.00 | -2.43 | -1.41 | 0/15 |
| canonical | 18.36 | -4.79 | -2.55 | 1/5 |
| blocks64 | 32.00 | -8.31 | -1.09 | 5/15 |

### by image (mean over masks and seeds)

| image | shipped - harmonic | converged - harmonic | converged - biharmonic | converged wins vs harmonic | cases |
|---|---|---|---|---|---|
| phantom | -0.82 | 0.92 | -0.33 | 11 | 19 |
| camera | -1.52 | -0.10 | 0.15 | 6 | 19 |
| astronaut | -1.24 | -0.40 | -1.08 | 7 | 19 |
| grass | -0.72 | -0.42 | 0.70 | 4 | 19 |
| smooth | -7.69 | -4.91 | -33.00 | 0 | 19 |

## Improvement of shipped TV over no restoration / mean fill (hole PSNR, dB; mean of all cases)

| comparison | mean dB gain |
|---|---|
| tv_shipped - damaged | 22.65 |
| tv_shipped - meanfill | 13.55 |

## Effect of the documented implementation defects (hole PSNR, dB)

| change | mean | max abs | min | max |
|---|---|---|---|---|
| return u_test instead of u (forward sweep) | 0.013 | 0.222 | -0.207 | 0.222 |
| symmetric R-B-R sweep instead of R-B (both u_test) | 0.134 | 1.792 | -1.792 | 1.273 |
| both corrections | 0.147 | 1.999 | -1.999 | 1.496 |

Shipped iterate `u`: max |u - f| on known pixels over all cases: median 0.42, max 2.94 grey levels; `u_test` violation max 0.0e+00.

## Metric sanity

Relative hole-RMSE change caused by clipping to [0,255]: max 1.17e-03, median 0.00e+00. Fraction of hole pixels outside [0,255] for `tv_shipped`: max 0.482, mean 0.0428.

## Convergence of the shipped setting (200 iterations) relative to the 1500-iteration reference

| mask | inradius | median rel dist to ref @200 | median TV excess @200 | mean dPSNR(200 - 1500) | mean gain of best checkpoint over 1500 |
|---|---|---|---|---|---|
| dropout | 1.609 | 0.0002315 | 1.668e-05 | -0.07835 | 0.008817 |
| blocks8 | 4 | 0.002713 | 3.209e-05 | 0.08641 | 0.1463 |
| scratch | 5.908 | 0.001891 | 3.341e-05 | -0.0848 | 0.08911 |
| blocks16 | 8 | 0.009358 | 0.0002249 | 0.072 | 0.1794 |
| blocks32 | 16 | 0.03661 | 0.00537 | -0.5986 | 0.2259 |
| canonical | 18.36 | 0.03243 | 0.001941 | -2.343 | 0.06767 |
| blocks64 | 32 | 0.1728 | 0.03857 | -6.643 | 0.1273 |

### rel distance to reference and hole PSNR by iteration (median/mean over all cases)

| k | median rel dist to ref | mean hole PSNR | median rel change of u |
|---|---|---|---|
| 10 | 0.3187 | 11.62 | 0.009818 |
| 25 | 0.2078 | 15.48 | 0.003942 |
| 50 | 0.09321 | 19.54 | 0.00228 |
| 100 | 0.02909 | 23.73 | 0.001184 |
| 200 | 0.003841 | 26.73 | 8.684e-05 |
| 300 | 0.001498 | 27.6 | 3.483e-05 |
| 500 | 0.0004967 | 28 | 4.439e-06 |
| 750 | 0.0001266 | 28.01 | 9.476e-07 |
| 1000 | 3.746e-05 | 28 | 3.146e-07 |
| 1500 | 0 | 28 | 3.371e-08 |

Checkpoint with the highest hole PSNR, count of cases: k=100: 11, k=200: 14, k=300: 18, k=500: 17, k=750: 12, k=1000: 3, k=1500: 20

## Failure-mode diagnostics inside the hole (mean over seeds)


**mask blocks32**  (truth row: diagnostics of the true image over the same hole)

| image | method | edge_retention | hf_retention | jump_conc | flat_frac | grad_ratio |
|---|---|---|---|---|---|---|
| phantom | truth | 1.000 | 1.000 | 0.478 | 0.000 | 1.000 |
| phantom | harmonic | 0.185 | 0.000 | 0.170 | 0.000 | 0.683 |
| phantom | biharmonic | 0.264 | 0.019 | 0.191 | 0.000 | 0.837 |
| phantom | tv_shipped | 0.119 | 0.158 | 0.292 | 0.000 | 0.717 |
| phantom | tv_converged | 0.184 | 0.172 | 0.542 | 0.000 | 0.358 |
| camera | truth | 1.000 | 1.000 | 0.104 | 0.088 | 1.000 |
| camera | harmonic | 0.097 | 0.000 | 0.126 | 0.367 | 0.193 |
| camera | biharmonic | 0.178 | 0.015 | 0.107 | 0.240 | 0.336 |
| camera | tv_shipped | 0.061 | 0.051 | 0.314 | 0.697 | 0.131 |
| camera | tv_converged | 0.077 | 0.056 | 0.404 | 0.812 | 0.112 |
| astronaut | truth | 1.000 | 1.000 | 0.104 | 0.093 | 1.000 |
| astronaut | harmonic | 0.135 | 0.000 | 0.080 | 0.133 | 0.346 |
| astronaut | biharmonic | 0.224 | 0.018 | 0.079 | 0.138 | 0.483 |
| astronaut | tv_shipped | 0.083 | 0.118 | 0.231 | 0.605 | 0.251 |
| astronaut | tv_converged | 0.112 | 0.106 | 0.247 | 0.651 | 0.232 |
| grass | truth | 1.000 | 1.000 | 0.047 | 0.014 | 1.000 |
| grass | harmonic | 0.063 | 0.000 | 0.092 | 0.513 | 0.135 |
| grass | biharmonic | 0.119 | 0.011 | 0.059 | 0.123 | 0.269 |
| grass | tv_shipped | 0.030 | 0.028 | 0.325 | 0.899 | 0.066 |
| grass | tv_converged | 0.029 | 0.029 | 0.332 | 0.903 | 0.064 |
| smooth | truth | 1.000 | 1.000 | 0.023 | 0.002 | 1.000 |
| smooth | harmonic | 0.971 | 0.000 | 0.025 | 0.001 | 0.987 |
| smooth | biharmonic | 0.999 | 0.992 | 0.023 | 0.002 | 1.000 |
| smooth | tv_shipped | 0.985 | 91.610 | 0.033 | 0.026 | 1.023 |
| smooth | tv_converged | 0.981 | 50.742 | 0.034 | 0.023 | 0.974 |

**mask blocks64**  (truth row: diagnostics of the true image over the same hole)

| image | method | edge_retention | hf_retention | jump_conc | flat_frac | grad_ratio |
|---|---|---|---|---|---|---|
| phantom | truth | 1.000 | 1.000 | 0.513 | 0.000 | 1.000 |
| phantom | harmonic | 0.145 | 0.000 | 0.184 | 0.000 | 0.548 |
| phantom | biharmonic | 0.215 | 0.014 | 0.194 | 0.000 | 0.732 |
| phantom | tv_shipped | 0.153 | 0.649 | 0.312 | 0.000 | 1.301 |
| phantom | tv_converged | 0.143 | 0.121 | 0.549 | 0.000 | 0.290 |
| camera | truth | 1.000 | 1.000 | 0.105 | 0.087 | 1.000 |
| camera | harmonic | 0.067 | 0.000 | 0.129 | 0.340 | 0.165 |
| camera | biharmonic | 0.135 | 0.008 | 0.115 | 0.163 | 0.285 |
| camera | tv_shipped | 0.030 | 0.235 | 0.453 | 0.807 | 0.206 |
| camera | tv_converged | 0.055 | 0.044 | 0.458 | 0.853 | 0.099 |
| astronaut | truth | 1.000 | 1.000 | 0.106 | 0.117 | 1.000 |
| astronaut | harmonic | 0.072 | 0.000 | 0.094 | 0.076 | 0.230 |
| astronaut | biharmonic | 0.132 | 0.010 | 0.093 | 0.173 | 0.351 |
| astronaut | tv_shipped | 0.037 | 0.206 | 0.446 | 0.747 | 0.208 |
| astronaut | tv_converged | 0.043 | 0.066 | 0.303 | 0.730 | 0.139 |
| grass | truth | 1.000 | 1.000 | 0.047 | 0.014 | 1.000 |
| grass | harmonic | 0.037 | 0.000 | 0.129 | 0.749 | 0.079 |
| grass | biharmonic | 0.081 | 0.006 | 0.074 | 0.275 | 0.187 |
| grass | tv_shipped | 0.020 | 0.026 | 0.522 | 0.947 | 0.045 |
| grass | tv_converged | 0.016 | 0.017 | 0.557 | 0.960 | 0.033 |
| smooth | truth | 1.000 | 1.000 | 0.022 | 0.001 | 1.000 |
| smooth | harmonic | 0.879 | 0.000 | 0.025 | 0.001 | 0.943 |
| smooth | biharmonic | 0.990 | 1.002 | 0.022 | 0.002 | 0.994 |
| smooth | tv_shipped | 0.523 | 133619.553 | 0.337 | 0.376 | 1.203 |
| smooth | tv_converged | 0.930 | 364.150 | 0.054 | 0.068 | 0.896 |

**mask canonical**  (truth row: diagnostics of the true image over the same hole)

| image | method | edge_retention | hf_retention | jump_conc | flat_frac | grad_ratio |
|---|---|---|---|---|---|---|
| phantom | truth | 1.000 | 1.000 | 0.641 | 0.000 | 1.000 |
| phantom | harmonic | 0.550 | 0.000 | 0.310 | 0.000 | 0.995 |
| phantom | biharmonic | 0.664 | 0.066 | 0.351 | 0.000 | 1.042 |
| phantom | tv_shipped | 0.684 | 0.268 | 0.398 | 0.000 | 1.138 |
| phantom | tv_converged | 0.718 | 0.272 | 0.540 | 0.000 | 0.868 |
| camera | truth | 1.000 | 1.000 | 0.111 | 0.093 | 1.000 |
| camera | harmonic | 0.236 | 0.000 | 0.127 | 0.226 | 0.385 |
| camera | biharmonic | 0.321 | 0.044 | 0.113 | 0.155 | 0.509 |
| camera | tv_shipped | 0.226 | 0.111 | 0.220 | 0.527 | 0.313 |
| camera | tv_converged | 0.233 | 0.110 | 0.226 | 0.546 | 0.305 |
| astronaut | truth | 1.000 | 1.000 | 0.107 | 0.094 | 1.000 |
| astronaut | harmonic | 0.379 | 0.000 | 0.102 | 0.116 | 0.586 |
| astronaut | biharmonic | 0.483 | 0.075 | 0.100 | 0.116 | 0.684 |
| astronaut | tv_shipped | 0.384 | 0.166 | 0.157 | 0.382 | 0.496 |
| astronaut | tv_converged | 0.390 | 0.157 | 0.156 | 0.386 | 0.494 |
| grass | truth | 1.000 | 1.000 | 0.047 | 0.013 | 1.000 |
| grass | harmonic | 0.200 | 0.000 | 0.058 | 0.213 | 0.346 |
| grass | biharmonic | 0.273 | 0.043 | 0.046 | 0.054 | 0.481 |
| grass | tv_shipped | 0.167 | 0.068 | 0.100 | 0.569 | 0.257 |
| grass | tv_converged | 0.167 | 0.069 | 0.100 | 0.571 | 0.256 |
| smooth | truth | 1.000 | 1.000 | 0.023 | 0.000 | 1.000 |
| smooth | harmonic | 1.000 | 0.000 | 0.024 | 0.000 | 0.998 |
| smooth | biharmonic | 1.000 | 0.922 | 0.023 | 0.000 | 1.000 |
| smooth | tv_shipped | 1.024 | 168.423 | 0.037 | 0.035 | 1.004 |
| smooth | tv_converged | 1.025 | 163.029 | 0.040 | 0.023 | 0.992 |

## Hole RMSE by distance to the nearest known pixel (mean over images and seeds)


**mask canonical**

| distance (px) | harmonic | biharmonic | tv_shipped | tv_converged |
|---|---|---|---|---|
| (0, 1] | 12.03 | 10.75 | 13.00 | 12.41 |
| (1, 2] | 15.99 | 15.03 | 17.62 | 15.72 |
| (2, 4] | 22.16 | 22.09 | 29.76 | 24.14 |
| (4, 8] | 25.93 | 27.95 | 36.31 | 27.94 |
| (8, 16] | 31.78 | 37.14 | 49.67 | 32.98 |
| (16, 32] | 34.84 | 48.20 | 49.53 | 22.18 |

**mask blocks32**

| distance (px) | harmonic | biharmonic | tv_shipped | tv_converged |
|---|---|---|---|---|
| (0, 1] | 15.09 | 13.92 | 25.56 | 24.77 |
| (1, 2] | 21.24 | 20.90 | 29.11 | 27.35 |
| (2, 4] | 26.00 | 26.88 | 32.23 | 29.87 |
| (4, 8] | 30.68 | 33.72 | 35.06 | 32.90 |
| (8, 16] | 34.38 | 38.97 | 37.71 | 35.71 |

**mask blocks64**

| distance (px) | harmonic | biharmonic | tv_shipped | tv_converged |
|---|---|---|---|---|
| (0, 1] | 15.15 | 13.48 | 59.61 | 27.81 |
| (1, 2] | 21.67 | 20.69 | 64.55 | 29.61 |
| (2, 4] | 25.96 | 26.47 | 69.01 | 30.96 |
| (4, 8] | 30.51 | 33.64 | 73.27 | 32.73 |
| (8, 16] | 34.32 | 39.82 | 73.93 | 35.38 |
| (16, 32] | 37.11 | 43.46 | 73.74 | 37.31 |

## Runtime (parallel run on a loaded machine; see serial timing for clean numbers)

| method | median s | p10 | p90 |
|---|---|---|---|
| harmonic | 0.07 | 0.05 | 0.15 |
| biharmonic | 0.10 | 0.06 | 0.30 |
| tv_shipped | 5.67 | 4.21 | 6.26 |
| tv_corrected | 7.24 | 5.39 | 7.96 |
| tv_converged | 52.73 | 37.37 | 59.76 |

## Parameter sensitivity on held-out development images


**S1_sigma**

| case | value | rmse_hole_u | rmse_hole_utest | tv_utest | hole_mean_u | truth_hole_mean | finite | runtime_s |
|---|---|---|---|---|---|---|---|---|
| moon+canonical | 2 | 62.87 | 62.74 | 6.103e+05 | 153.4 | 112.6 | True | 5.327 |
| moon+canonical | 5 | 32.51 | 32.33 | 4.79e+05 | 128.2 | 112.6 | True | 5.258 |
| moon+canonical | 8 | 16.79 | 16.63 | 4.465e+05 | 118.3 | 112.6 | True | 5.558 |
| moon+canonical | 14 | 4.939 | 4.937 | 4.334e+05 | 112 | 112.6 | True | 5.059 |
| moon+canonical | 25 | 4.507 | 4.542 | 4.327e+05 | 112.4 | 112.6 | True | 5.194 |
| moon+canonical | 50 | 5.754 | 5.787 | 4.358e+05 | 112.9 | 112.6 | True | 5.194 |
| moon+blocks32 | 2 | 104.2 | 104 | 7.921e+05 | 212.4 | 110.1 | True | 4.675 |
| moon+blocks32 | 5 | 56.55 | 56.16 | 6.036e+05 | 164.1 | 110.1 | True | 4.954 |
| moon+blocks32 | 8 | 15.23 | 14.89 | 4.366e+05 | 118.6 | 110.1 | True | 4.185 |
| moon+blocks32 | 14 | 7.807 | 7.793 | 4.233e+05 | 109.4 | 110.1 | True | 4.109 |
| moon+blocks32 | 25 | 7.215 | 7.245 | 4.229e+05 | 110.1 | 110.1 | True | 4.424 |
| moon+blocks32 | 50 | 8.582 | 8.533 | 4.316e+05 | 114.4 | 110.1 | True | 4.516 |
| coins+blocks32 | 2 | 121.5 | 121.4 | 1.62e+06 | 212.6 | 105.5 | True | 2.185 |
| coins+blocks32 | 5 | 85.11 | 84.87 | 1.532e+06 | 169.5 | 105.5 | True | 2.295 |
| coins+blocks32 | 8 | 63.61 | 63.39 | 1.493e+06 | 141.1 | 105.5 | True | 2.238 |
| coins+blocks32 | 14 | 41.51 | 41.4 | 1.457e+06 | 107.4 | 105.5 | True | 2.319 |
| coins+blocks32 | 25 | 43.02 | 43.07 | 1.446e+06 | 90.4 | 105.5 | True | 2.244 |
| coins+blocks32 | 50 | 46.88 | 46.88 | 1.445e+06 | 88.68 | 105.5 | True | 2.239 |

**S2_sweeps**

| case | value | rmse_hole_u | rmse_hole_utest | tv_utest | hole_mean_u | truth_hole_mean | finite | runtime_s |
|---|---|---|---|---|---|---|---|---|
| moon+canonical | 1 | 24.29 | 24.12 | 4.606e+05 | 122.6 | 112.6 | True | 2.989 |
| moon+canonical | 2 | 7.025 | 6.868 | 4.357e+05 | 113.9 | 112.6 | True | 4.273 |
| moon+canonical | 3 | 4.939 | 4.937 | 4.334e+05 | 112 | 112.6 | True | 4.907 |
| moon+canonical | 5 | 4.557 | 4.574 | 4.321e+05 | 112.7 | 112.6 | True | 7.594 |
| moon+canonical | 10 | 4.398 | 4.38 | 4.314e+05 | 112.8 | 112.6 | True | 12.95 |
| moon+blocks32 | 1 | 34.83 | 34.34 | 5.192e+05 | 141.5 | 110.1 | True | 2.604 |
| moon+blocks32 | 2 | 8.819 | 8.829 | 4.269e+05 | 112.7 | 110.1 | True | 3.285 |
| moon+blocks32 | 3 | 7.807 | 7.793 | 4.233e+05 | 109.4 | 110.1 | True | 4.148 |
| moon+blocks32 | 5 | 7.365 | 7.363 | 4.208e+05 | 111.7 | 110.1 | True | 6.356 |
| moon+blocks32 | 10 | 7.174 | 7.168 | 4.194e+05 | 111.3 | 110.1 | True | 11.88 |
| coins+blocks32 | 1 | 73.11 | 72.88 | 1.51e+06 | 153.6 | 105.5 | True | 1.309 |
| coins+blocks32 | 2 | 49.45 | 49.25 | 1.472e+06 | 121.2 | 105.5 | True | 1.771 |
| coins+blocks32 | 3 | 41.51 | 41.4 | 1.457e+06 | 107.4 | 105.5 | True | 2.255 |
| coins+blocks32 | 5 | 39.32 | 39.32 | 1.45e+06 | 97.88 | 105.5 | True | 3.291 |
| coins+blocks32 | 10 | 39.79 | 39.83 | 1.448e+06 | 94.33 | 105.5 | True | 5.832 |

**S3_iterations**

| case | value | rmse_hole_u | rmse_hole_utest | tv_utest | hole_mean_u | truth_hole_mean | finite | runtime_s | rel_dist_to_2000 |
|---|---|---|---|---|---|---|---|---|---|
| moon+canonical | 10 | 85.07 | 83.26 | 1.006e+06 | 182 | 112.6 | True |  | 0.2976 |
| moon+canonical | 25 | 66.97 | 66.06 | 6.441e+05 | 156.1 | 112.6 | True |  | 0.2359 |
| moon+canonical | 50 | 46.4 | 45.67 | 5.39e+05 | 140.3 | 112.6 | True |  | 0.1625 |
| moon+canonical | 100 | 21.71 | 21.38 | 4.575e+05 | 121.1 | 112.6 | True |  | 0.07457 |
| moon+canonical | 200 | 4.939 | 4.937 | 4.334e+05 | 112 | 112.6 | True |  | 0.009678 |
| moon+canonical | 300 | 4.329 | 4.328 | 4.311e+05 | 112.4 | 112.6 | True |  | 0.002655 |
| moon+canonical | 500 | 4.299 | 4.299 | 4.307e+05 | 112.6 | 112.6 | True |  | 0.0003469 |
| moon+canonical | 1000 | 4.304 | 4.304 | 4.307e+05 | 112.6 | 112.6 | True |  | 3.262e-05 |
| moon+canonical | 2000 | 4.305 | 4.305 | 4.307e+05 | 112.6 | 112.6 | True |  | 0 |
| moon+blocks32 | 10 | 127 | 125.8 | 9e+05 | 235.3 | 110.1 | True |  | 0.4429 |
| moon+blocks32 | 25 | 109.4 | 108.2 | 8.307e+05 | 217.6 | 110.1 | True |  | 0.3802 |
| moon+blocks32 | 50 | 80.8 | 79.67 | 6.998e+05 | 188.6 | 110.1 | True |  | 0.2781 |
| moon+blocks32 | 100 | 27.54 | 26.58 | 4.892e+05 | 133.8 | 110.1 | True |  | 0.08496 |
| moon+blocks32 | 200 | 7.807 | 7.793 | 4.233e+05 | 109.4 | 110.1 | True |  | 0.009332 |
| moon+blocks32 | 300 | 7.077 | 7.075 | 4.188e+05 | 110.9 | 110.1 | True |  | 0.001849 |
| moon+blocks32 | 500 | 6.959 | 6.959 | 4.182e+05 | 110.9 | 110.1 | True |  | 0.0001977 |
| moon+blocks32 | 1000 | 6.958 | 6.958 | 4.182e+05 | 110.9 | 110.1 | True |  | 2.442e-05 |
| moon+blocks32 | 2000 | 6.958 | 6.958 | 4.182e+05 | 110.9 | 110.1 | True |  | 0 |
| coins+blocks32 | 10 | 141.6 | 140.6 | 1.681e+06 | 234.9 | 105.5 | True |  | 0.5659 |
| coins+blocks32 | 25 | 126 | 125 | 1.642e+06 | 217.6 | 105.5 | True |  | 0.5033 |
| coins+blocks32 | 50 | 102 | 101.1 | 1.574e+06 | 190.3 | 105.5 | True |  | 0.4064 |
| coins+blocks32 | 100 | 68.22 | 67.77 | 1.502e+06 | 147.6 | 105.5 | True |  | 0.2592 |
| coins+blocks32 | 200 | 41.51 | 41.4 | 1.457e+06 | 107.4 | 105.5 | True |  | 0.1065 |
| coins+blocks32 | 300 | 40.4 | 40.44 | 1.447e+06 | 92.71 | 105.5 | True |  | 0.04464 |
| coins+blocks32 | 500 | 45.09 | 45.1 | 1.445e+06 | 89.46 | 105.5 | True |  | 0.01794 |
| coins+blocks32 | 1000 | 46.82 | 46.83 | 1.445e+06 | 88.46 | 105.5 | True |  | 0.004187 |
| coins+blocks32 | 2000 | 47.13 | 47.13 | 1.445e+06 | 88.29 | 105.5 | True |  | 0 |

**S4_sigma_tau**

| case | value | rmse_hole_u | rmse_hole_utest | tv_utest | hole_mean_u | truth_hole_mean | finite | runtime_s |
|---|---|---|---|---|---|---|---|---|
| moon+blocks32 | 0.25|False | nan | nan | nan | nan | 110.1 | False | 6.736 |
| moon+blocks32 | 0.25|True | 22.56 | 23.53 | 5.203e+05 | 121.9 | 110.1 | True | 6.675 |
| moon+blocks32 | 0.5|False | nan | nan | nan | nan | 110.1 | False | 6.888 |
| moon+blocks32 | 0.5|True | 10.73 | 11.1 | 4.458e+05 | 105.7 | 110.1 | True | 6.55 |
| moon+blocks32 | 1.0|False | 7.807 | 7.793 | 4.233e+05 | 109.4 | 110.1 | True | 6.815 |
| moon+blocks32 | 1.0|True | 7.807 | 7.793 | 4.233e+05 | 109.4 | 110.1 | True | 7.518 |
| moon+blocks32 | 2.0|False | 129.5 | 129.5 | 4.39e+40 | -9.64e+31 | 110.1 | True | 6.762 |
| moon+blocks32 | 2.0|True | 40.77 | 40.34 | 5.429e+05 | 147.8 | 110.1 | True | 7.243 |
| moon+blocks32 | 4.0|False | 129.5 | 129.5 | 2.782e+55 | -1.808e+47 | 110.1 | True | 7.309 |
| moon+blocks32 | 4.0|True | 104.2 | 104 | 7.941e+05 | 211.3 | 110.1 | True | 7.527 |

**S5_init**

| case | value | rmse_hole_u | rmse_hole_utest | tv_utest | hole_mean_u | truth_hole_mean | finite | runtime_s |
|---|---|---|---|---|---|---|---|---|
| moon+canonical | white(shipped) | 4.939 | 4.937 | 4.334e+05 | 112 | 112.6 | True | 5.256 |
| moon+canonical | known-mean | 4.304 | 4.304 | 4.308e+05 | 112.6 | 112.6 | True | 5.009 |
| moon+canonical | harmonic | 4.294 | 4.295 | 4.308e+05 | 112.6 | 112.6 | True | 4.71 |
| moon+blocks32 | white(shipped) | 7.807 | 7.793 | 4.233e+05 | 109.4 | 110.1 | True | 4.926 |
| moon+blocks32 | known-mean | 7.047 | 7.045 | 4.184e+05 | 110.9 | 110.1 | True | 4.813 |
| moon+blocks32 | harmonic | 6.928 | 6.928 | 4.183e+05 | 110.9 | 110.1 | True | 4.878 |
| coins+blocks32 | white(shipped) | 41.51 | 41.4 | 1.457e+06 | 107.4 | 105.5 | True | 3.492 |
| coins+blocks32 | known-mean | 45.48 | 45.49 | 1.445e+06 | 87.43 | 105.5 | True | 3.871 |
| coins+blocks32 | harmonic | 44.45 | 44.46 | 1.445e+06 | 89.35 | 105.5 | True | 3.996 |

## Noise on the known pixels (canonical mask, shipped TV), mean over noise seeds

| image | noise sd | noisy obs hole | full | harmonic hole | full | biharmonic hole | full | tv_shipped hole | full |
|---|---|---|---|---|---|---|---|---|---|
| astronaut | 0.00 | 3.90 | 11.80 | 20.82 | 28.72 | 21.96 | 29.86 | 17.69 | 25.59 |
| astronaut | 5.00 | 3.90 | 11.78 | 20.78 | 27.81 | 21.73 | 28.57 | 17.65 | 25.10 |
| astronaut | 15.00 | 3.90 | 11.63 | 20.56 | 23.92 | 20.21 | 23.80 | 17.39 | 22.53 |
| astronaut | 30.00 | 3.90 | 11.19 | 19.94 | 19.33 | 17.31 | 18.85 | 16.81 | 18.73 |
| camera | 0.00 | 4.01 | 11.91 | 20.95 | 28.85 | 20.33 | 28.23 | 19.69 | 27.59 |
| camera | 5.00 | 4.01 | 11.89 | 20.94 | 27.90 | 20.18 | 27.27 | 19.64 | 26.82 |
| camera | 15.00 | 4.01 | 11.73 | 20.76 | 23.86 | 19.06 | 23.22 | 19.39 | 23.36 |
| camera | 30.00 | 4.01 | 11.28 | 20.18 | 19.34 | 16.78 | 18.70 | 18.79 | 19.13 |
| phantom | 0.00 | 0.83 | 8.73 | 23.49 | 31.38 | 24.69 | 32.58 | 18.18 | 26.07 |
| phantom | 5.00 | 0.83 | 8.72 | 23.45 | 30.19 | 24.27 | 30.80 | 18.17 | 25.69 |
| phantom | 15.00 | 0.83 | 8.66 | 23.19 | 25.55 | 22.17 | 25.23 | 18.04 | 23.41 |
| phantom | 30.00 | 0.83 | 8.48 | 22.39 | 20.63 | 18.71 | 20.04 | 17.62 | 19.78 |
| smooth | 0.00 | 5.38 | 13.28 | 59.75 | 67.64 | 94.52 | 102.42 | 46.09 | 53.99 |
| smooth | 5.00 | 5.38 | 13.25 | 42.90 | 34.82 | 34.11 | 34.15 | 40.22 | 34.72 |
| smooth | 15.00 | 5.38 | 13.02 | 33.45 | 25.29 | 24.56 | 24.62 | 33.98 | 25.30 |
| smooth | 30.00 | 5.38 | 12.35 | 27.45 | 19.39 | 18.63 | 18.72 | 29.17 | 19.43 |
