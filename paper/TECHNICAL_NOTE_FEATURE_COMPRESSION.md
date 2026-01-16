# Evidence-first Feature Compression: A Reproducible Evaluation Surface (Technical Note)

**Author**: 陈铭（Independent）  
**Date**: 2026-01-16  

## Abstract

Feature compression and collaborative inference are often discussed in terms of model structure and training tricks, but teams frequently stall on **evaluation**: inconsistent environments, unclear baselines, and missing evidence artifacts. This technical note proposes an **evidence-first evaluation surface** for feature compression under bandwidth constraints. The contribution is not a new compression algorithm; instead, it standardizes what should be shipped and reviewed: `env/results/report/manifest` plus a minimal release gate. A small toy experiment is provided to demonstrate **rate/distortion** reporting and reproducible artifact generation without any private data or weights.

## 1. Scope (what this is / is not)

- This note is about **engineering methodology** for research-to-delivery.
- It is **not** a claim of SOTA feature compression.
- It does **not** ship weights, private datasets, calibration tables, or internal implementations.

## 2. Problem: evaluation drift in compression projects

In practice, feature compression projects suffer from:

- **Baseline drift**: “what we compared against” changes silently over time.
- **Methodology drift**: different tokenization / pre-processing / runtime flags produce incomparable numbers.
- **Evidence drift**: results are shared as screenshots, not as auditable artifacts.

## 3. Evidence-first evaluation surface

This repo defines a minimal public Evidence Pack:

- `env.json`: environment fingerprint
- `results.json`: structured metrics + minimal methodology fields
- `report.md`: one-page human-readable summary
- `manifest.json`: integrity manifest (SHA-256)

The claim boundary is simple: **only what is backed by these artifacts is claimed**.

## 4. Toy experiment: rate/distortion + bandwidth sanity check

To keep the public boundary clean, we include a toy experiment that is:

- offline (no external data)
- easy to reproduce
- still aligned with the feature compression shape (tensor → quantize → transmit → reconstruct)

### 4.1 Method

Generate synthetic feature vectors \(X \in \mathbb{R}^{N \times D}\). Apply per-dimension linear quantization at 2/4/8 bits, reconstruct \(\hat{X}\), and report:

- **Rate**: bits per element (bpe)
- **Distortion**: MSE \(\mathbb{E}[(X-\hat{X})^2]\)
- **Payload latency (toy)**: payload size divided by assumed bandwidth (not an end-to-end system claim)

### 4.2 Reproduction

- Entry: `SW_PUBLIC/examples/feature_compression_toy/`
- Run:

```powershell
pwsh .\examples\feature_compression_toy\run.ps1
```

Outputs:

- `examples/feature_compression_toy/artifacts/env.json`
- `examples/feature_compression_toy/artifacts/results.json`
- `examples/feature_compression_toy/artifacts/report.md`
- `examples/feature_compression_toy/artifacts/manifest.json`

## 5. Discussion: why this is “research-capable”

A research team’s throughput is often limited by “everything around the algorithm”:

- standardized baselines
- comparable metrics
- reproducible scripts
- artifact integrity and reviewability

This is a valid systems contribution: it makes future algorithm iterations faster, safer, and easier to validate across devices.

## 6. Limitations

- The toy is not a real video/point-cloud pipeline.
- Latency is a payload-only estimate; real systems include compute, scheduling, and network variability.
- Real quality metrics (e.g., task accuracy, perception quality) are out of scope unless accompanied by public evidence under the same methodology.

## 7. Pointers

- Public audit gate: `SW_PUBLIC/scripts/audit_public.ps1`
- Reproduce guide: `SW_PUBLIC/REPRODUCE.md`
- Measurement notes: `SW_PUBLIC/MEASURE.md`


