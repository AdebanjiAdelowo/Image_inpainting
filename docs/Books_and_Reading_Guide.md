---
title: "Books and Reading Guide"
subtitle: "A Structured Study Roadmap for TV Inpainting via Preconditioned Douglas-Rachford Splitting"
author: "Adebanji Oluwatimileyin Adelowo"
date: "2026"
toc: true
toc-depth: 3
number-sections: true
geometry: margin=1in
fontsize: 11pt
linkcolor: blue
urlcolor: blue
---

# How to Use This Guide

## What this document is

This is a **study roadmap**, not a bibliography. The companion document,
*Total Variation Image Inpainting via Preconditioned Douglas-Rachford
Splitting* (referred to throughout as **the technical document**), cites 34
sources — mostly research papers, together with three books ([2], [3], [34])
and one technical report ([12], the repository's primary algorithmic
reference) — and derives
every formula the repository implements. Those sources are primary; they are
terse, and most of them assume a body of background that is found in books
rather than in papers.

This guide names those books, says precisely **which parts of each one matter
for this project**, and explains **what to extract** from each. Every entry
answers the same six questions:

1. What is it, exactly (title, edition, publisher, year, ISBN, DOI or publisher
   page)?
2. Why is it relevant to *this* project, as opposed to imaging in general?
3. Which topics in the technical document does it underwrite?
4. Which chapters or sections should actually be read?
5. What level is it written at, and is it foundational, supplementary, or
   advanced here?
6. Where does it sit in the reading order, and which of the cited papers does it
   prepare the reader for?

Eighteen books are included. Each was checked against a publisher, library, or
bookseller record for edition, year and ISBN; nothing here is quoted from
memory.

**Conventions.** "TD §7.6.3" refers to a section of the *technical document*.
"Section 4.4" or "Sec. 4.4" refers to a section of *this guide*. Bracketed
numbers such as [12] are the technical document's bibliography entries.
Chapter references inside a book entry are to that book. Where a book's chapter
numbering could not be confirmed against the publisher's own table of contents,
the chapter is named rather than numbered.

## The four questions this project raises

The repository is small — roughly eighty lines of NumPy — but it sits at the
intersection of four distinct literatures, and a reader who wants to
*understand* rather than merely *run* it needs something from each.

**(A) Why this model?** Why minimize total variation subject to a hard data
constraint, rather than any of the alternatives? This is a question about
variational image models and about the space $\mathrm{BV}$: it is answered by
the imaging books of Section 3 and the analysis books of Section 5.

**(B) Why this reformulation?** Why does a non-smooth, one-homogeneous
functional become a saddle-point problem with two projections? This is convex
analysis: conjugates, subdifferentials, proximal operators, Fenchel-Rockafellar
duality (Section 4).

**(C) Why this algorithm?** Why Douglas-Rachford, why a preconditioner, and why
does an inexact inner solve not destroy convergence? This is monotone-operator
theory and operator splitting (Section 4), plus the primary papers themselves.

**(D) Why this inner solver?** Why red-black Gauss-Seidel, why symmetrize it,
and what would replace it at scale? This is numerical linear algebra
(Section 6) — and, as the technical document shows in its Section 7.6.3, it is
exactly the point at which the repository's implementation departs from the
theory it instantiates.

Sections 7 and 8 of this guide add context: general image processing, and the
learned methods that now dominate the inpainting literature.

## Coverage map

The following table maps each major section of the technical document to the
book that best prepares a reader for it. Numbers in brackets are the reference
numbers used in the technical document's bibliography.

| Technical document section | Primary book | Secondary |
|---|---|---|
| 1. Introduction, applications | Szeliski (Sec. 7.2) | Gonzalez-Woods (Sec. 7.1) |
| 2. Problem formulation, well-posedness | Aubert-Kornprobst (Sec. 3.3) | Schönlieb (Sec. 3.1) |
| 3.1 BV and the TV seminorm, coarea | Ambrosio-Fusco-Pallara (Sec. 5.1) | Aubert-Kornprobst |
| 3.2 Convex analysis, conjugates | Rockafellar (Sec. 4.2), Brezis (Sec. 5.2) | Boyd-Vandenberghe (Sec. 4.5) |
| 3.3 Proximal operators | Parikh-Boyd (Sec. 4.4), Beck (Sec. 4.3) | Bauschke-Combettes (Sec. 4.1) |
| 3.4 Saddle points, duality | Boyd-Vandenberghe (Sec. 4.5) | Rockafellar (Sec. 4.2) |
| 4. Classical inpainting methods | Schönlieb (Sec. 3.1) | Chan-Shen (Sec. 3.2) |
| 5. Research evolution | Chan-Shen (Sec. 3.2), Scherzer et al. (Sec. 3.4) | Szeliski (Sec. 7.2) |
| 6. Douglas-Rachford, preconditioning | Bauschke-Combettes (Sec. 4.1) | Beck (Sec. 4.3) |
| 7.1-7.5 Discretization, adjointness | Chambolle-Pock papers [6, 7] | Aubert-Kornprobst (Sec. 3.3) |
| 7.6 Red-black Gauss-Seidel | Saad (Sec. 6.1) | Briggs et al. (Sec. 6.2) |
| 8. Code implementation | — (this repository) | Gonzalez-Woods (Sec. 7.1) |
| 9. Experiments, convergence, timing | — (this repository; see Sec. 10) | Briggs et al. (Sec. 6.2) |
| 10. Limitations (staircasing, texture) | Schönlieb (Sec. 3.1), Chan-Shen (Sec. 3.2) | Scherzer et al. (Sec. 3.4) |
| 11.1-11.3 Future work: TGV, multigrid | Briggs et al. (Sec. 6.2) | Scherzer et al. (Sec. 3.4) |
| 11.6 Hybrid classical/learned | Prince (Sec. 8.2) | Goodfellow et al. (Sec. 8.1) |

## Levels and roles

Each entry is tagged with a **level** — *advanced undergraduate*, *graduate*, or
*research monograph* — and a **role** for this project:

* **Foundational** — the project's mathematics cannot be understood without at
  least the named chapters.
* **Supplementary** — fills in context, alternatives, or breadth; valuable but
  skippable on a first pass.
* **Advanced** — the reference to reach for when the foundational treatment is
  not precise enough, or when extending the work.

# Reading Roadmap

## The three-book fast track

A reader with a solid undergraduate mathematics background who wants to
understand the repository completely, and has time for three books, should read:

1. **Parikh and Boyd, *Proximal Algorithms*** (Section 4.4) — about 110 pages,
   free online. Delivers the proximal operator, the Moreau decomposition, and
   the splitting-algorithm family, which is most of the technical document's
   Sections 3.3 and 6.
2. **Schönlieb, *Partial Differential Equation Methods for Image Inpainting***
   (Section 3.1) — the only book devoted to this exact problem. Delivers the
   modelling context of Sections 2, 4 and 10.
3. **Saad, *Iterative Methods for Sparse Linear Systems***, the basic-iterative-
   methods chapter (Section 6.1) — delivers Gauss-Seidel, its red-black
   ordering, symmetrization and the preconditioner formalism of Section 7.6.

Everything else in this guide is depth behind one of those three.

## Ordered reading paths by background

**Path 1 — coming from applied mathematics or numerical analysis.**
Saad (basic iterative methods) $\to$ Boyd-Vandenberghe (Chapters 3 and 5)
$\to$ Parikh-Boyd $\to$ Bauschke-Combettes (the monotone-operator and
Douglas-Rachford chapters) $\to$ Schönlieb $\to$ Ambrosio-Fusco-Pallara
(Chapter 3, as reference). This is the shortest route to reading the
Bredies-Sun papers [12, 13] with full comprehension.

**Path 2 — coming from image processing or computer vision.**
Gonzalez-Woods (restoration chapter) $\to$ Szeliski (regularization and
computational-photography material) $\to$ Chan-Shen $\to$ Schönlieb $\to$
Aubert-Kornprobst $\to$ Boyd-Vandenberghe $\to$ Parikh-Boyd. Here the risk is
skipping the convex analysis; do not.

**Path 3 — coming from optimization.**
Rockafellar or Bauschke-Combettes (as reference) $\to$ Beck (subgradients,
conjugates, the proximal operator) $\to$ the Chambolle-Pock survey [7] $\to$
Schönlieb $\to$ Ambrosio-Fusco-Pallara. The imaging side is what needs filling
in: specifically why $\mathrm{BV}$ and not $H^1$.

**Path 4 — coming from deep learning.**
Prince (Chapter 18) $\to$ Szeliski $\to$ Schönlieb $\to$ Boyd-Vandenberghe
$\to$ Parikh-Boyd. The goal is to see the classical method as a prior plus a
constraint, which is precisely the structure that plug-and-play and unrolled
architectures reuse (technical document, Section 11.6).

## A twelve-week study plan

| Weeks | Focus | Reading | Outcome |
|---|---|---|---|
| 1-2 | Image models, why TV | Schönlieb Ch. 1-4; Chan-Shen introductory and denoising chapters | Can state (2.1) and say why not $H^1$ |
| 3-4 | BV and the TV seminorm | Ambrosio-Fusco-Pallara Ch. 3; Aubert-Kornprobst mathematical preliminaries | Can prove lower semicontinuity; understands coarea |
| 5-6 | Convex analysis | Boyd-Vandenberghe Ch. 3, 5; Beck Ch. 3, 4 | Can derive the conjugate of a norm, (3.6) |
| 7 | Proximal operators | Parikh-Boyd §1-2, 6; Beck Ch. 6 | Can derive both proximal steps of the code |
| 8-9 | Monotone operators, splitting | Bauschke-Combettes (monotone operators, resolvents, Douglas-Rachford) | Can read Lions-Mercier [10] and Eckstein-Bertsekas [11] |
| 10 | The primary papers | Bredies-Sun [12, 13]; Chambolle-Pock [6] | Can derive the PDR box of Section 6.4 |
| 11 | The inner solver | Saad Ch. 4; Briggs et al. Ch. 1-3 | Understands feasibility, red-black, and multigrid as the upgrade |
| 12 | Modern context | Prince Ch. 18; the learned-inpainting papers [27-32] | Can situate the project in the current literature |

# Tier 1: Image Inpainting and Variational Imaging

These four books address the problem the repository solves. If only one book is
read, it should be the first.

## Schönlieb, *Partial Differential Equation Methods for Image Inpainting*

**Full details.** Carola-Bibiane Schönlieb, *Partial Differential Equation
Methods for Image Inpainting*. Cambridge Monographs on Applied and
Computational Mathematics, No. 29. Cambridge University Press, 2015.
ISBN 978-1-107-00100-8.
Publisher page: <https://www.cambridge.org/core/books/partial-differential-equation-methods-for-image-inpainting/>

**Level.** Graduate / research monograph. **Role: foundational.**

**Why it matters here.** This is the only book-length treatment of image
inpainting as a mathematical problem, written by one of the field's principal
contributors. Everything the technical document says in its Sections 4 and 10 —
why harmonic inpainting blurs edges, why TV continues them straight, why
curvature-based models were invented, when each method succeeds — is developed
here properly, with proofs, rather than summarized in a paragraph. It is also
the book that explains the *geometry* of the inpainting domain: why the width of
the hole rather than its area governs the outcome, which is exactly the point
the technical document's Section 9.1 makes empirically with the mask's inradius
statistics.

**Topics it underwrites.** The principle of good continuation and the
connectivity principle; second-order diffusion inpainting (harmonic, TV) and its
failure modes; higher-order equations (Cahn-Hilliard, TV-$H^{-1}$, elastica) and
why they reconnect contours where TV cannot; transport-based inpainting; the
Mumford-Shah image model; and the relationship between transport and diffusion
mechanisms.

**What to read.** The chapter on *The Principle of Good Continuation*, which
frames the whole subject; *Second-Order Diffusion Equations for Inpainting*,
which contains the harmonic and TV models of the technical document's
Sections 4.1 and 2.3; the higher-order-equation chapter, which is the
theoretical basis for the TGV direction proposed in Section 11.1; *Transport
Inpainting*, which is Bertalmío et al. [19] done rigorously; *The Mumford-Shah
Image Model for Inpainting*; and *Inpainting Mechanisms of Transport and
Diffusion*, which is the synthesis. The appendices cover the mathematical
preliminaries and a MATLAB implementation, and are worth having open alongside
the repository's notebooks.

**How it connects to the code.** Indirectly but deeply: it tells the reader what
to expect from the output *before* running it. The flat polygonal patches inside
the large blob in the technical document's Section 9.3 are not a bug, and this
book is where that is established.

**Relation to the cited papers.** It is the systematic version of references
[19], [20], [21], [22], [23] and [33], and it cites and contextualizes all of
them.

**Reading order.** First, or immediately after a fast pass through the technical
document.

## Chan and Shen, *Image Processing and Analysis*

**Full details.** Tony F. Chan and Jianhong (Jackie) Shen, *Image Processing and
Analysis: Variational, PDE, Wavelet, and Stochastic Methods*. Society for
Industrial and Applied Mathematics (SIAM), Philadelphia, 2005.
DOI: 10.1137/1.9780898717877. This is reference [34] of the technical document.

**Level.** Graduate. **Role: foundational.**

**Why it matters here.** Chan and Shen wrote most of the founding papers on
variational inpainting ([21], [22], [24]), and this book is their own unified
account. It is the single best source for *why the modelling choices are what
they are* — the Bayesian and variational rationales side by side — and it treats
inpainting as one instance of a family that also includes denoising, deblurring
and segmentation, which is how the technical document's Section 5 organizes the
history.

**Topics it underwrites.** Image modelling and representation (why an image is
usefully modelled as a BV function); the ROF model and TV denoising; the
inpainting chapter, containing the harmonic and TV inpainting analyses and the
connectivity-principle discussion; the relationship between the variational,
PDE, wavelet and stochastic viewpoints.

**What to read.** The chapters on *image modeling and representation*, on *image
denoising* (which is where TV enters, and the direct source for the technical
document's Section 5.1), and on *image inpainting*. The earlier chapter on
modern image analysis tools is a useful compressed reference for the measure
theory and PDE background if Ambrosio-Fusco-Pallara is too heavy.

**How it connects to the code.** The inpainting chapter's analysis of TV
inpainting is the theory of which `proximalG` plus the TV term is the
discretization. Its discussion of when TV fails to reconnect contours is the
model-level explanation of the limitation catalogued in the technical document's
Section 10.1.

**Relation to the cited papers.** It is the book form of [21], [22] and [24],
and it predates and motivates the algorithmic literature ([12]-[16]) rather than
covering it.

**Reading order.** Alongside or just after Schönlieb; they overlap productively,
with Chan-Shen stronger on modelling and Schönlieb stronger on PDE analysis and
higher-order methods.

## Aubert and Kornprobst, *Mathematical Problems in Image Processing*

**Full details.** Gilles Aubert and Pierre Kornprobst, *Mathematical Problems in
Image Processing: Partial Differential Equations and the Calculus of
Variations*. 2nd edition. Applied Mathematical Sciences, Vol. 147. Springer, New
York, 2006. ISBN 978-0-387-32200-1.
Publisher page: <https://link.springer.com/book/10.1007/978-0-387-44588-5>

**Level.** Graduate. **Role: foundational** for the analysis, **supplementary**
for the algorithms.

**Why it matters here.** This is the book that supplies the *rigour* the
technical document's Section 2.4 gestures at: existence of minimizers by the
direct method, lower semicontinuity, compactness in BV, and the precise sense in
which a variational imaging problem is well posed. Its mathematical
preliminaries chapter is a self-contained course in exactly the analysis an
imaging person needs — BV functions, $\Gamma$-convergence, viscosity solutions —
without the full generality of a measure-theory monograph.

**Topics it underwrites.** The direct method of the calculus of variations;
functions of bounded variation and their use as an image model; the ROF model
and its analysis; regularization and the choice of exponent in
$\int|\nabla u|^p$; discretization of PDE-based image models; and, in the later
chapters, applications including disocclusion and inpainting.

**What to read.** The *mathematical preliminaries* chapter (BV, lower
semicontinuity, the direct method) is the core: it underwrites the technical
document's Sections 2.4 and 3.1. Then the *image restoration* chapter for the
ROF model and the general variational framework, and the applications chapter
for the inpainting/disocclusion material.

**How it connects to the code.** It justifies the claim that (2.1) has a
solution at all, and it explains why the discrete problem inherits that
property. It also treats the discretization of variational imaging models in
general, which is the subject of the technical document's Section 7.

**Relation to the cited papers.** It is the analytical companion to [1] and
[22], and its BV material is a gentler entry to [2].

**Reading order.** After Schönlieb, before or alongside Ambrosio-Fusco-Pallara.

## Scherzer, Grasmair, Grossauer, Haltmeier and Lenzen, *Variational Methods in Imaging*

**Full details.** Otmar Scherzer, Markus Grasmair, Harald Grossauer, Markus
Haltmeier and Frank Lenzen, *Variational Methods in Imaging*. Applied
Mathematical Sciences, Vol. 167. Springer, New York, 2009.
ISBN 978-0-387-30931-6. DOI: 10.1007/978-0-387-69277-7.

**Level.** Graduate / research monograph. **Role: supplementary.**

**Why it matters here.** It frames variational imaging as *regularization theory
for inverse problems*, which is the viewpoint that generalizes the repository
beyond inpainting. In that language, inpainting is the inverse problem whose
forward operator is multiplication by the mask; TV is the regularizer; and the
hard constraint of (2.1) is the zero-noise limit. Reading the project this way
makes the extensions of the technical document's Section 11 obvious rather than
inventive.

**Topics it underwrites.** Regularization functionals and their properties;
convex regularization and duality in the imaging context; existence, stability
and convergence of regularized solutions; the general framework into which TGV
[17] and higher-order regularizers fit.

**What to read.** The chapters on variational regularization methods and on
convex regularization for denoising. The treatment of convex duality there is a
useful bridge between the abstract statements of Boyd-Vandenberghe and the
imaging-specific use made in the technical document's Section 3.5.

**How it connects to the code.** It supplies the vocabulary — forward operator,
regularizer, discrepancy, parameter choice — in which one would extend
`tv_inpainting` to deblurring or tomography by changing $K$ and the data term
while keeping the entire splitting machinery.

**Relation to the cited papers.** Provides the inverse-problems framing for
[1], [17] and, indirectly, the whole algorithmic line [5]-[16].

**Reading order.** After the Tier 1 books and the convex analysis of Tier 2;
this is the book that makes the project generalize.

# Tier 2: Convex Analysis, Monotone Operators and Proximal Algorithms

This tier answers questions (B) and (C) of Section 1.2. The repository's entire
algorithm is an instance of material in these five books.

## Bauschke and Combettes, *Convex Analysis and Monotone Operator Theory in Hilbert Spaces*

**Full details.** Heinz H. Bauschke and Patrick L. Combettes, *Convex Analysis
and Monotone Operator Theory in Hilbert Spaces*. 2nd edition. CMS Books in
Mathematics. Springer, Cham, 2017. ISBN 978-3-319-48310-8.
DOI: 10.1007/978-3-319-48311-5.

**Level.** Graduate / research monograph. **Role: foundational** for Section 6
of the technical document — this is *the* reference for the theory the
Bredies-Sun papers assume.

**Why it matters here.** Every object in the technical document's Section 6 —
maximal monotone operator, resolvent, firm non-expansiveness, Fejér
monotonicity, demiclosedness, the Douglas-Rachford operator itself — is defined
and developed here, in Hilbert space, at exactly the level of generality the
primary papers use. Bredies and Sun prove weak convergence "in Hilbert space
under minimal assumptions"; this is the book in which the reader learns what
those words mean and why weak convergence is the natural mode.

**Topics it underwrites.** Conjugation and the Fenchel-Moreau theorem
(TD §3.2.4); subdifferentiability and Fermat's rule (TD §3.2.3);
proximity operators, including their firm non-expansiveness and the Moreau
decomposition (TD §3.3); monotone operators and maximal monotonicity (TD §6.1);
resolvents and their relation to proximity operators (TD §3.3.1, equation 3.8);
and the algorithms for finding zeros of sums of monotone operators, which is
where Douglas-Rachford lives (TD §6.2).

**What to read.** By chapter title, in this order: *Conjugation*;
*Subdifferentiability*; *Proximity Operators*; *Monotone Operators*;
*Resolvents of Monotone Operators*; and *Zeros of Sums of Monotone Operators*,
which contains the Douglas-Rachford splitting algorithm and its convergence
proof. Also worth having: the material on projections onto convex sets, which is
what both of the repository's proximal routines compute.

**How it connects to the code.** `proximalFstar` and `proximalG` are proximity
operators of indicator functions, i.e. projections, i.e. resolvents of normal
cone operators — three descriptions of the same seven lines of NumPy, all three
defined in this book. The two "reflection" lines of `tv_inpainting`
(`u_bar + u_test - u`) are the Douglas-Rachford update in its standard form,
which appears here with a proof of why it converges.

**Relation to the cited papers.** It is the modern textbook home of [10]
(Lions-Mercier), [11] (Eckstein-Bertsekas) and [8] (Combettes-Pesquet, by one of
the same authors); it is the background assumed by [12] and [13].

**Reading order.** After a first pass through Parikh-Boyd or Beck; it is a
reference to consult rather than a book to read linearly.

## Rockafellar, *Convex Analysis*

**Full details.** R. Tyrrell Rockafellar, *Convex Analysis*. Princeton
Landmarks in Mathematics and Physics. Princeton University Press, 1970
(paperback edition 1997). ISBN 978-0-691-01586-6. This is reference [3] of the
technical document.

**Level.** Graduate / research monograph. **Role: advanced reference.**

**Why it matters here.** It is the origin of the finite-dimensional theory the
project uses, and the source of the duality theorem that carries the
"Fenchel-Rockafellar" name in the technical document's Section 3.4 and in
Bredies and Sun's paper. When a statement about conjugates, subgradients or
saddle functions needs to be checked exactly, this is where it is settled.

**Topics it underwrites.** Convex sets and functions; the Legendre-Fenchel
transform and its properties (TD §3.2.4); subgradients and
subdifferential calculus (TD §3.2.3); saddle functions, minimax theorems, and
Fenchel duality (TD §3.4).

**What to read.** The parts on conjugate convex functions and on
subdifferentiation, then the material on saddle functions and minimax. The
technical document's equation (3.6) — the conjugate of a norm is the indicator
of the dual-norm ball — and the saddle-point characterization (3.17) are both
theorems here.

**How it connects to the code.** It supplies the theorem that turns
$\alpha\|\nabla u\|_{2,1}$ into $\delta_{B_\alpha}(p)$, which is the single
step that converts the repository's problem into one with two closed-form
projections.

**Relation to the cited papers.** Cited directly by [12] and by essentially
every other optimization reference in the technical document.

**Reading order.** Reference only; do not read linearly for this project.
Bauschke-Combettes covers the same ground with modern notation and Hilbert-space
generality.

## Beck, *First-Order Methods in Optimization*

**Full details.** Amir Beck, *First-Order Methods in Optimization*. MOS-SIAM
Series on Optimization, Vol. 25. SIAM, Philadelphia, 2017.
ISBN 978-1-611974-98-0. DOI: 10.1137/1.9781611974997.

**Level.** Graduate. **Role: foundational** — the most efficient single source
for the proximal calculus this project needs.

**Why it matters here.** Beck's treatment of the proximal operator is the
clearest available, and — crucially for this project — it includes an extensive
*calculus* of proximal operators with worked examples, including exactly the two
the repository implements: the projection onto a Euclidean ball and the
projection onto an affine set defined by fixing coordinates. The technical
document's derivations (3.11) and (3.12) are special cases of results tabulated
here.

**Topics it underwrites.** Subgradients and subdifferential calculus
(TD §3.2.3); conjugate functions and the conjugate of a norm (TD §3.2.4); the
proximal operator, its properties, the Moreau decomposition, and closed-form
formulas (TD §3.3); first-order methods including proximal gradient and, in later
chapters, primal-dual and ADMM-type schemes (TD §5.2).

**What to read.** Chapter 3 (*Subgradients*), Chapter 4 (*Conjugate
Functions*), and Chapter 6 (*The Proximal Operator*) are the core — they map
almost one-to-one onto the technical document's Section 3. Then the chapters on
the proximal gradient method and on primal-dual/ADMM-type methods for the
algorithmic context of Section 5.2.

**How it connects to the code.** The formula
$\Pi_B(p) = p/\max(1, \|p\|/\rho)$ implemented in `proximalFstar` and the
coordinate-fixing projection implemented in `proximalG` are both derived in the
proximal-operator chapter. Reading it makes the two functions obvious rather
than mysterious.

**Relation to the cited papers.** The textbook companion to [8], and the
background for [5], [6] and [15].

**Reading order.** Early — this and Parikh-Boyd are the two most efficient
sources for Section 3 of the technical document.

## Parikh and Boyd, *Proximal Algorithms*

**Full details.** Neal Parikh and Stephen Boyd, *Proximal Algorithms*.
Foundations and Trends in Optimization, Vol. 1, No. 3, pp. 127-239, 2014.
now publishers. ISBN 978-1-60198-716-7. DOI: 10.1561/2400000003.
Freely available at <https://web.stanford.edu/~boyd/papers/prox_algs.html>

**Level.** Advanced undergraduate to graduate. **Role: foundational**, and the
single best value for time in this entire guide.

**Why it matters here.** It is short (about 110 pages), free, and covers exactly
the machinery the repository uses, with an engineer's emphasis on what a
proximal operator *does* and how to evaluate it. The interpretations chapter —
prox as a gradient step on the Moreau envelope, as a trust-region step, as a
resolvent — is the fastest way to acquire intuition for why the technical
document's Section 6 works at all.

**Topics it underwrites.** The definition and properties of the proximal
operator (TD §3.3.1); fixed points and the resolvent identity (equation 3.8); the
Moreau decomposition (equation 3.9); proximal point, proximal gradient and ADMM
(TD §5.2, TD §6.2); and closed-form proximal operators for the standard building
blocks, including projection onto balls and affine sets, and soft thresholding
(TD §3.3.3-3.3.5).

**What to read.** All of it, but at minimum: the introduction and the properties
chapter for the definition, the resolvent identity and the Moreau
decomposition; the interpretations chapter for intuition; the proximal-
algorithms chapter for the proximal point method, which is the frame in which
Bredies and Sun reformulate Douglas-Rachford (TD §6.3); and the
chapter on evaluating proximal operators, which contains the two formulas the
repository implements.

**How it connects to the code.** More directly than any other book here: the
technical document's Section 3.3 is essentially a specialization of this
monograph to the two functions in (3.18).

**Relation to the cited papers.** Written by the authors of the ADMM literature
that [15] belongs to; the natural companion to [8]; and the shortest path to
being able to read [12] and [13].

**Reading order.** First among the optimization books.

## Boyd and Vandenberghe, *Convex Optimization*

**Full details.** Stephen Boyd and Lieven Vandenberghe, *Convex Optimization*.
Cambridge University Press, 2004. ISBN 978-0-521-83378-3.
Freely available at <https://web.stanford.edu/~boyd/cvxbook/>

**Level.** Advanced undergraduate to graduate. **Role: foundational** for
duality and saddle points.

**Why it matters here.** It is the standard reference for the duality machinery
of the technical document's Section 3.4, and its treatment of the conjugate
function and of the saddle-point interpretation of duality is the most readable
anywhere. It is also the book most readers will already have.

**Topics it underwrites.** Convex sets and functions; the conjugate function
(TD §3.2.4); Lagrange duality and, specifically, the saddle-point interpretation
that turns a min into a min-max (TD §3.4); optimality conditions.

**What to read.** Chapter 2 (*Convex sets*) selectively; Chapter 3 (*Convex
functions*), especially §3.3 on the conjugate function; Chapter 4 (*Convex
optimization problems*) for the role of indicator functions and constraints; and
Chapter 5 (*Duality*), especially §5.4, the saddle-point interpretation, which
is the abstract version of the technical document's equation (3.16).

**How it connects to the code.** It explains why the two-variable formulation
solved by `tv_inpainting` — one primal image $u$, one dual vector field $p$ — is
equivalent to the one-variable constrained problem the README states.

**Relation to the cited papers.** Background for [6], [7] and [8]; the duality
it teaches in finite dimensions is what [12] and [13] use in Hilbert space.

**Reading order.** Before or alongside Parikh-Boyd. Chapters 3 and 5 suffice for
this project.

# Tier 3: Functional-Analytic and PDE Foundations

These three books supply the ambient mathematics: the space in which images
live, the Hilbert-space vocabulary the algorithm is stated in, and the PDE
theory behind the classical inpainting models.

## Ambrosio, Fusco and Pallara, *Functions of Bounded Variation and Free Discontinuity Problems*

**Full details.** Luigi Ambrosio, Nicola Fusco and Diego Pallara, *Functions of
Bounded Variation and Free Discontinuity Problems*. Oxford Mathematical
Monographs. Oxford University Press, 2000. ISBN 978-0-19-850245-6. This is
reference [2] of the technical document.

**Level.** Research monograph. **Role: advanced reference** — authoritative, and
demanding.

**Why it matters here.** Every claim the technical document makes about
$\mathrm{BV}(\Omega)$ is a theorem in this book: the dual definition of total
variation, the decomposition of the distributional derivative into absolutely
continuous, jump and Cantor parts, lower semicontinuity under $L^1$ convergence,
compactness, and the coarea formula. The coarea formula in particular is the
engine behind the entire geometric interpretation of TV — "minimizing the total
length of level lines" — on which the technical document's Sections 2.3, 3.1.2
and 10.1 all rest.

**Topics it underwrites.** The definition of total variation as a supremum over
test vector fields (TD equation 3.1); $Du$ as a Radon measure and
$\mathrm{TV}(u)=|Du|(\Omega)$; the jump set and the meaning of an "edge" in a BV
function; lower semicontinuity and compactness, hence existence of minimizers
(TD §2.4); and the coarea formula (TD equation 3.2).

**What to read.** Chapter 3, on functions of bounded variation, is the relevant
one: the definition and basic properties, the structure theorem for $Du$,
compactness and lower semicontinuity, and the coarea formula. Chapters 1 and 2
(measure theory, Hausdorff measures, rectifiability) are prerequisites to
consult as needed rather than to read through. The later free-discontinuity
material is background for the Mumford-Shah models mentioned in the technical
document's Section 4.3, not for TV itself.

**How it connects to the code.** Only indirectly — the code works in
finite dimensions, where none of this is needed. Its value is in explaining
*why the discrete problem is the right discretization*: the discrete TV (2.4)
is a consistent approximation of a functional that is well behaved in the
continuum, which is what makes the results mesh-independent in the appropriate
sense and what justifies calling $p$ a discrete test field.

**Relation to the cited papers.** It is the standard citation behind [1], [17],
[22] and [24] whenever BV is invoked.

**Reading order.** As a reference throughout; a targeted reading of the BV
chapter is worthwhile after Aubert-Kornprobst's gentler treatment.

## Brezis, *Functional Analysis, Sobolev Spaces and Partial Differential Equations*

**Full details.** Haim Brezis, *Functional Analysis, Sobolev Spaces and Partial
Differential Equations*. Universitext. Springer, New York, 2011.
ISBN 978-0-387-70913-0. DOI: 10.1007/978-0-387-70914-7.

**Level.** Graduate. **Role: foundational** for the functional-analytic
vocabulary.

**Why it matters here.** The technical document works in a Hilbert space $H$
throughout Section 3 and speaks of weak convergence, adjoint operators,
projections onto closed convex sets, and maximal monotone operators. Brezis
develops all of these from scratch, and — unusually for a functional analysis
text — devotes an early chapter to *conjugate convex functions*, which is
exactly the tool the technical document's Section 3.2.4 needs.

**Topics it underwrites.** Hahn-Banach and the theory of conjugate convex
functions (TD §3.2.4); Hilbert spaces, the projection theorem for closed convex
sets (TD §3.3.2, the fact that makes both proximal steps projections), and
adjoint operators (TD §7.3); weak topologies and weak convergence, which is the
mode of convergence in the Bredies-Sun theorem (TD §6.6); maximal monotone
operators and the Hille-Yosida theorem, which is where resolvents
$(I+\lambda A)^{-1}$ first appear; and Sobolev spaces, needed to say precisely
why $H^1$ functions cannot jump (TD §2.3).

**What to read.** Chapter 1, on the Hahn-Banach theorems and conjugate convex
functions, especially the sections on the Legendre transform; Chapter 3, on weak
topologies, for the meaning of weak convergence; Chapter 5, on Hilbert spaces,
for the projection theorem and adjoints; Chapter 7, on the Hille-Yosida theorem,
for maximal monotone operators and resolvents; and Chapters 8-9 on Sobolev
spaces for the $H^1$ comparison.

**How it connects to the code.** The projection theorem is the reason
`proximalG` and `proximalFstar` are well defined and single-valued; the adjoint
material is the abstract version of the discrete adjointness proof of the
technical document's Section 7.3.

**Relation to the cited papers.** Background for [10], [11] and [12], all of
which are stated in Hilbert space.

**Reading order.** Reference; read the conjugate-functions and Hilbert-space
chapters before tackling Bauschke-Combettes.

## Evans, *Partial Differential Equations*

**Full details.** Lawrence C. Evans, *Partial Differential Equations*. 2nd
edition. Graduate Studies in Mathematics, Vol. 19. American Mathematical
Society, Providence, 2010. ISBN 978-0-8218-4974-3.

**Level.** Graduate. **Role: supplementary** — but the right book for Section 4
of the technical document.

**Why it matters here.** The classical inpainting methods that TV displaced are
PDE methods, and the technical document's Section 4.1 makes claims about them
that are theorems in Evans: harmonic functions are smooth in the interior (so
harmonic inpainting cannot preserve an edge), the maximum principle forbids new
extrema (so texture is annihilated), and the Dirichlet principle identifies
energy minimization with the Laplace equation. The direct method of the calculus
of variations, used in the technical document's Section 2.4, is also developed
here in the $W^{1,p}$ setting.

**Topics it underwrites.** Laplace's equation: the mean-value property, the
maximum principle, smoothness of harmonic functions, and the Dirichlet
principle (TD §4.1); the heat equation as the gradient flow of the Dirichlet
energy (TD §4.1); the direct method in the calculus of variations, existence of
minimizers, and Euler-Lagrange equations (TD §2.4).

**What to read.** Chapter 2, §2.2 on Laplace's equation — the properties of
harmonic functions are the entire argument against harmonic inpainting — and
§2.3 on the heat equation. Then Chapter 8, on the calculus of variations,
especially the sections on the direct method and the existence of minimizers.

**How it connects to the code.** The linear system the inner solver attacks,
$(\lambda I - \mu\Delta)u = b$, is a screened Poisson equation; Evans is where
one learns what its solutions look like and why the operator is coercive.

**Relation to the cited papers.** Background for [19], [20], [21], [23] and
[33] — all PDE-based inpainting models.

**Reading order.** Consult when reading Section 4 of the technical document.

# Tier 4: Numerical Linear Algebra and the Inner Solver

The repository's most interesting engineering decision is its inner solver, and
its most significant defect (technical document, Section 7.6.3) is in that
solver's symmetry. These two books cover it exactly.

## Saad, *Iterative Methods for Sparse Linear Systems*

**Full details.** Yousef Saad, *Iterative Methods for Sparse Linear Systems*.
2nd edition. SIAM, Philadelphia, 2003. ISBN 978-0-89871-534-7.
DOI: 10.1137/1.9780898718003.
Freely available at <https://www-users.cse.umn.edu/~saad/books.html>

**Level.** Graduate. **Role: foundational** for the technical document's
Section 7.6.

**Why it matters here.** `sym_red_black_gauss_seidel` is a textbook object, and
this is the textbook. Everything the technical document derives in Section 7.6 —
the Gauss-Seidel update as a splitting $T = M_0 - (M_0 - T)$, the multicolour
(red-black) ordering that decouples the updates within a colour, the
symmetrized forward-backward sweep (SSOR/SGS), and the notion of a
preconditioner as an approximate inverse — is standard material here, developed
with the convergence theory that the technical document's numerical experiment
in Section 7.6.3 tests empirically.

**Topics it underwrites.** Matrix splittings and stationary iterative methods;
Jacobi, Gauss-Seidel, SOR and SSOR, including their convergence for symmetric
positive definite and for diagonally dominant matrices (TD §7.5); multicolour
orderings and their use for parallelism (TD §7.6.2); preconditioning as a
concept, and the specific preconditioners induced by these splittings
(TD §6.5).

**What to read.** Chapter 4, *Basic Iterative Methods*, is the core: the
splitting formalism, Jacobi/Gauss-Seidel/SOR/SSOR, and their convergence
theory. Follow it with the treatment of multicolour and red-black orderings in
the sparse-matrix and parallel-implementation chapters, which explain why the
checkerboard is chosen and how it vectorizes. Chapter 10, *Preconditioning
Techniques*, gives the general picture into which the Bredies-Sun notion of a
*feasible* preconditioner fits as a special, stronger requirement.

**How it connects to the code.** Directly and completely. In particular, the
distinction between a forward sweep ($M_0 = D - E$, non-symmetric) and the
symmetrized sweep ($M = M_0(M_0+M_0^*-T)^{-1}M_0^*$) that the technical
document's Section 7.6.3 shows the repository conflates, is standard SSOR/SGS
material in this book. A reader who has worked through Chapter 4 will spot the
issue immediately.

**Relation to the cited papers.** It is the numerical-linear-algebra background
assumed by [12, §4.2] and by the split Bregman literature [15].

**Reading order.** Early if the reader's interest is the implementation; the
basic-iterative-methods chapter can be read independently of everything else in
this guide.

## Briggs, Henson and McCormick, *A Multigrid Tutorial*

**Full details.** William L. Briggs, Van Emden Henson and Steve F. McCormick,
*A Multigrid Tutorial*. 2nd edition. SIAM, Philadelphia, 2000.
ISBN 978-0-89871-462-3. DOI: 10.1137/1.9780898719505.

**Level.** Advanced undergraduate to graduate. **Role: supplementary**, and the
right starting point for the technical document's Section 11.3.

**Why it matters here.** It explains, better than any other short text, *why*
Gauss-Seidel behaves as it does: it damps oscillatory error components quickly
and smooth ones very slowly. That single fact explains the convergence profile
measured in the technical document's Section 9.4 (fast initial progress, long
tail) and the observation in Section 10.2 that the iteration count must grow
with the width of the hole, since information enters the hole at roughly one
pixel per sweep. It then shows the standard cure — coarse-grid correction — and
gives V-cycles and full multigrid in complete, implementable detail.

**Topics it underwrites.** Model problems and the discrete Laplacian; the
smoothing property of relaxation methods, in Fourier terms (TD §11.3);
red-black Gauss-Seidel as a smoother; coarse-grid correction, restriction and
prolongation; V-cycles and full multigrid.

**What to read.** Chapters 1-3 are enough: *Model Problems* (the five-point
Laplacian, exactly the operator $T$ of the technical document's equation 7.7),
*Basic Iterative Methods* (the smoothing analysis), and *Elements of Multigrid*.
Chapter 4 on implementation is worth reading before attempting the multigrid
preconditioner proposed in Section 11.3.

**How it connects to the code.** It gives the diagnosis for the repository's
scaling behaviour, and the recipe for the upgrade: a symmetric multigrid V-cycle
for $I - \sigma^2\Delta$ is a candidate feasible preconditioner within the same
convergence theory, and would make the outer iteration count nearly independent
of hole size.

**Relation to the cited papers.** Not cited in the technical document; it is the
background for the extension proposed there in Section 11.3.

**Reading order.** After Saad's basic-iterative-methods chapter.

# Tier 5: Digital Image Processing and Computer Vision

Neither of these books teaches the mathematics of this project. Both supply the
practical and historical context in which it sits, and both are the natural
place to look for the *engineering* of images, as opposed to their analysis.

## Gonzalez and Woods, *Digital Image Processing*

**Full details.** Rafael C. Gonzalez and Richard E. Woods, *Digital Image
Processing*. 4th edition. Pearson, New York, 2018. ISBN 978-0-13-335672-4.
Approximately 1022 pages.

**Level.** Advanced undergraduate. **Role: supplementary** — general grounding.

**Why it matters here.** It is the standard reference for the conventions the
repository takes for granted: what an image array is, how greyscale intensities
are quantized to $[0,255]$, what pixel neighbourhoods and connectivity mean
(the 4-connectivity of `neighbor_sum` and of the mask's connected-component
analysis in the technical document's Section 9.1), how masks and spatial
filters work, and what "image restoration" means as an engineering discipline.
For a reader coming to this project without an imaging background, it removes a
surprising number of small obstacles.

**Topics it underwrites.** Digital image fundamentals: sampling, quantization,
pixel adjacency and connectivity, distance measures (TD §9.1); intensity
transformations and spatial filtering, including the Laplacian as a sharpening
filter (TD §7.4); image restoration and reconstruction as a framework
(TD §1.2); and, in the 4th edition, an introduction to deep learning and
convolutional networks that connects to Section 8 of this guide.

**What to read.** The chapter on digital image fundamentals — particularly the
sections on neighbourhoods, adjacency and connectivity, which are what the mask
statistics of the technical document's Section 9.1 measure — and the chapter on
image restoration and reconstruction. The spatial-filtering chapter's treatment
of the discrete Laplacian is a useful concrete complement to the operator
algebra of the technical document's Section 7.4.

**How it connects to the code.** It explains the data: why `u0.png` is an RGB
file whose three channels are identical, what taking the red channel does, and
why clipping to $[0,255]$ before display is necessary.

**Caveat.** It does *not* cover variational inpainting; do not look for the
project's mathematics here.

**Relation to the cited papers.** None directly; it is the engineering
substrate.

**Reading order.** Before everything else if the reader has no imaging
background; otherwise skip.

## Szeliski, *Computer Vision: Algorithms and Applications*

**Full details.** Richard Szeliski, *Computer Vision: Algorithms and
Applications*. 2nd edition. Texts in Computer Science. Springer, Cham, 2022.
ISBN 978-3-030-34371-2. DOI: 10.1007/978-3-030-34372-9.
Draft freely available at <https://szeliski.org/Book/>

**Level.** Advanced undergraduate to graduate. **Role: supplementary** — the
best single-volume map of the surrounding field.

**Why it matters here.** It places inpainting where practitioners actually
encounter it: inside computational photography, alongside hole filling,
texture synthesis, image stitching and object removal. It also covers
regularization and energy minimization for vision problems from the practical
side — variational formulations, discrete MRF/graph-cut alternatives, and the
optimization methods used for each — which is useful perspective on why a
convex, continuous formulation was chosen here rather than a combinatorial one.
The 2nd edition is current enough to cover the learned methods of references
[27]-[32] in context.

**Topics it underwrites.** Regularization and energy-based formulations for
vision (TD §5); texture synthesis and exemplar-based hole filling, i.e. the
methods of references [25] and [26] (TD §4.4); computational photography,
including inpainting and object removal as applications (TD §1.2); and modern
deep architectures for image synthesis (TD §5.3).

**What to read.** The chapter covering model fitting, regularization and energy
minimization, for the alternative optimization traditions; and the
computational-photography chapter, for hole filling, texture synthesis and
inpainting in practice. The bibliographic notes at the end of each chapter are
unusually good and are an efficient way to find further literature.

**How it connects to the code.** Weakly — but it is the book that answers "where
would I actually deploy this, and what would I be compared against?"

**Relation to the cited papers.** Surveys and contextualizes [25], [26] and the
learned line [27]-[32].

**Reading order.** Any time; useful early for motivation, and again at the end
for perspective.

# Tier 6: Deep-Learning Context

The technical document's Sections 1.3, 5.3 and 11.6 argue that the classical
method remains valuable *and* that the field has moved on. These two books
support the second half of that claim. Neither is needed to understand the
repository.

## Goodfellow, Bengio and Courville, *Deep Learning*

**Full details.** Ian Goodfellow, Yoshua Bengio and Aaron Courville, *Deep
Learning*. Adaptive Computation and Machine Learning series. MIT Press,
Cambridge, MA, 2016. ISBN 978-0-262-03561-3.
Freely available at <https://www.deeplearningbook.org/>

**Level.** Graduate. **Role: supplementary** — context only.

**Why it matters here.** It is the standard reference for the vocabulary of the
learned methods that the technical document cites in Section 5.3 — convolutional
networks, adversarial training, generative models — and it makes explicit the
one structural comparison that matters for this project: a learned inpainting
network is a *prior* fitted to data, where TV is a prior asserted a priori.
Chapter-level treatment of regularization also makes the analogy between weight
decay, early stopping and variational regularization concrete.

**Topics it underwrites.** Regularization in learned models, as the counterpart
of the variational regularization of TD §2.3; convolutional networks, the
architecture of references [27]-[30]; generative modelling and adversarial
training, the mechanism of [27] and [28].

**What to read.** The chapters on regularization for deep learning, on
convolutional networks, and on deep generative models. Nothing else is needed
for this project's purposes.

**Relation to the cited papers.** Background for [27], [28] and [29].

**Reading order.** Last, and optional.

## Prince, *Understanding Deep Learning*

**Full details.** Simon J. D. Prince, *Understanding Deep Learning*. MIT Press,
Cambridge, MA, 2023. ISBN 978-0-262-04864-4.
Freely available at <https://udlbook.github.io/udlbook/>

**Level.** Advanced undergraduate to graduate. **Role: supplementary** —
context, but the more current of the two.

**Why it matters here.** Its Chapter 18 is a clear, self-contained treatment of
**diffusion models**, which are the current state of the art for inpainting
large holes and are cited in the technical document as references [31] and [32].
For a reader who wants to understand the hybrid direction proposed in
Section 11.6 — a learned prior with a classical data-consistency projection —
this chapter plus the technical document's Section 3.3 is exactly the required
combination: the projection step used by diffusion inpainting samplers *is*
`proximalG`.

**Topics it underwrites.** Diffusion models and their sampling procedures
(TD §5.3, references [31], [32]); generative adversarial networks (references
[27], [28]); the general architecture vocabulary of references [29] and [30].

**What to read.** Chapter 18, *Diffusion models*, which begins on page 348 of
the print edition; the chapter on generative adversarial networks for the
earlier line of work; and the convolutional-network chapter if Goodfellow et al.
is not being read.

**How it connects to the code.** More directly than one would expect: the
"replace-the-known-pixels-at-every-step" trick used by diffusion inpainting
methods is a projection onto the same constraint set $C$ that `proximalG`
projects onto. Seeing that identity is the clearest possible demonstration that
the classical and learned methods share a skeleton.

**Relation to the cited papers.** Background for [31] and [32].

**Reading order.** Last; read Chapter 18 before the technical document's
Section 11.6.

# From Books to Papers

Books give the machinery; the primary papers give this specific algorithm. The
following table shows which book prepares the reader for which cited paper, so
that the papers can be read without stalling.

| Paper (technical document reference) | Read first |
|---|---|
| Rudin-Osher-Fatemi [1] | Chan-Shen (Sec. 3.2); Aubert-Kornprobst (Sec. 3.3) |
| Chambolle [5], Chambolle-Pock [6] | Boyd-Vandenberghe Ch. 3, 5; Parikh-Boyd |
| Chambolle-Pock survey [7] | Beck; Bauschke-Combettes (as reference) |
| Combettes-Pesquet [8] | Parikh-Boyd; Bauschke-Combettes |
| Douglas-Rachford [9] | Briggs et al. Ch. 1-2 (the ADI context); Evans Ch. 2 |
| Lions-Mercier [10], Eckstein-Bertsekas [11] | Bauschke-Combettes (monotone operators, resolvents) |
| **Bredies-Sun [12], [13], [14]** | **Bauschke-Combettes + Saad Ch. 4 + Boyd-Vandenberghe Ch. 5** |
| Goldstein-Osher [15], Getreuer [16] | Parikh-Boyd (ADMM); Saad Ch. 4 |
| Bredies-Kunisch-Pock (TGV) [17] | Ambrosio-Fusco-Pallara Ch. 3; Scherzer et al. |
| Strong-Chan [18] | Chan-Shen; Aubert-Kornprobst |
| Bertalmío et al. [19], Masnou-Morel [20] | Schönlieb; Evans Ch. 2 |
| Chan-Shen [21], [22], [24]; elastica [23] | Schönlieb; Chan-Shen |
| Criminisi et al. [25], Efros-Leung [26] | Szeliski (computational photography) |
| Learned inpainting [27]-[30] | Goodfellow et al.; Prince; Szeliski |
| Diffusion inpainting [31], [32] | Prince Ch. 18 |
| Bertozzi et al. [33] | Schönlieb (higher-order equations) |

The emphasized row is the one that matters most: the repository implements
[12]/[13], and those papers assume simultaneous fluency in monotone-operator
theory, stationary iterative methods, and convex duality. That combination —
Bauschke-Combettes, Saad, Boyd-Vandenberghe — is the real prerequisite list for
this project.

# What No Book Covers

Three things in this project are not in any book, and must be taken from the
papers or from the technical document itself.

1. **The preconditioned Douglas-Rachford method.** As of writing, PDR appears in
   the journal literature ([12], [13], [14]) and in surveys, but not in a
   textbook. The notion of a *feasible preconditioner* — $M$ self-adjoint,
   positive definite, with $M - T$ positive semi-definite — and the theorem that
   *any* number of inner sweeps preserves convergence, are specific to those
   papers. Bauschke-Combettes gives the Douglas-Rachford theory; Saad gives the
   preconditioners; the combination is the papers' contribution.

2. **The specific discretization used here.** The forward-difference gradient
   with the matching backward-difference divergence, and the adjointness
   identity that pairs them, are stated in Chambolle [5] and Chambolle-Pock [6]
   and are folklore elsewhere. The technical document's Section 7.3 gives the
   full proof for the repository's exact implementation.

3. **The repository's own behaviour.** The measurements in the technical
   document's Section 9 — convergence profile, runtime, parameter sensitivity,
   the verification of the operator identities, and the analysis in Section
   7.6.3 showing that the implemented sweep is forward rather than symmetric —
   exist only there.

# Summary Table

| # | Book | Year | Level | Role | Read for |
|---|---|---|---|---|---|
| 1 | Schönlieb, *PDE Methods for Image Inpainting* | 2015 | Grad | Foundational | The problem itself; TD §2, §4, §10 |
| 2 | Chan & Shen, *Image Processing and Analysis* | 2005 | Grad | Foundational | Variational image models; TD §4, §5 |
| 3 | Aubert & Kornprobst, *Mathematical Problems in Image Processing* | 2006 | Grad | Foundational | Well-posedness, BV in imaging; TD §2.4 |
| 4 | Scherzer et al., *Variational Methods in Imaging* | 2009 | Grad | Supplementary | Inverse-problems framing; TD §11 |
| 5 | Bauschke & Combettes, *Convex Analysis and Monotone Operator Theory* | 2017 | Grad | Foundational | Monotone operators, DR; TD §6 |
| 6 | Rockafellar, *Convex Analysis* | 1970 | Grad | Advanced ref. | Conjugates, saddle points; TD §3.2, §3.4 |
| 7 | Beck, *First-Order Methods in Optimization* | 2017 | Grad | Foundational | Prox calculus; TD §3.3 |
| 8 | Parikh & Boyd, *Proximal Algorithms* | 2014 | UG/Grad | Foundational | Proximal operators; TD §3.3, §6 |
| 9 | Boyd & Vandenberghe, *Convex Optimization* | 2004 | UG/Grad | Foundational | Duality, saddle points; TD §3.4 |
| 10 | Ambrosio, Fusco & Pallara, *Functions of Bounded Variation* | 2000 | Research | Advanced ref. | BV, coarea; TD §3.1 |
| 11 | Brezis, *Functional Analysis, Sobolev Spaces and PDE* | 2011 | Grad | Foundational | Hilbert spaces, conjugates; TD §3 |
| 12 | Evans, *Partial Differential Equations* | 2010 | Grad | Supplementary | Harmonic functions, direct method; TD §4.1 |
| 13 | Saad, *Iterative Methods for Sparse Linear Systems* | 2003 | Grad | Foundational | Gauss-Seidel, red-black; TD §7.6 |
| 14 | Briggs, Henson & McCormick, *A Multigrid Tutorial* | 2000 | UG/Grad | Supplementary | Smoothing, multigrid; TD §11.3 |
| 15 | Gonzalez & Woods, *Digital Image Processing* | 2018 | UG | Supplementary | Image fundamentals; TD §9.1 |
| 16 | Szeliski, *Computer Vision* | 2022 | UG/Grad | Supplementary | Field context; TD §4.4, §5.3 |
| 17 | Goodfellow, Bengio & Courville, *Deep Learning* | 2016 | Grad | Supplementary | Learned-method vocabulary; TD §5.3 |
| 18 | Prince, *Understanding Deep Learning* | 2023 | UG/Grad | Supplementary | Diffusion models; TD §11.6 |

"TD" denotes the technical document, *Total Variation Image Inpainting via
Preconditioned Douglas-Rachford Splitting*, in the same `docs/` directory.
