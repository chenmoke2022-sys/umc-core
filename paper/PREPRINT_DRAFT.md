# UMC: A Reproducible, Auditable, and Rollback-Ready Evidence Pack for Edge LLM Deployment

**Author**: 陈铭  
**Affiliation**: Independent  
**Contact**: https://github.com/chenmoke2022-sys/umc-core  
**Date**: 2026-01-14  

---

## Abstract

Edge and consumer deployments of large language models (LLMs) confront the “last-mile trust problem”: quantization and packaging decisions are often opaque, results are hard to reproduce across heterogeneous environments, and rollbacks are handled informally. I present **UMC (Universal Model Container)** as an engineering evidence standard: a minimal, structured **Evidence Pack** consisting of `env.json`, `results.json`, `report.md`, and an integrity `manifest.json`, plus a release gate that validates completeness and forbids sensitive leakage. I designed UMC to be **reproducible**, **auditable**, and **rollback-ready**. I am releasing an open, baseline-measured public pack and a toolchain that regenerates artifacts and enforces audit gates. My goal is not to claim unverified performance improvements, but to standardize the *verification surface* so that future candidate artifacts can be evaluated under a consistent methodology.

---

## 1. Introduction

### 1.1 Motivation
Deploying LLMs on edge devices (phones/IoT/embedded) requires aggressive packaging and optimization under strict constraints: memory budgets, cold-start latency, stability gates, and operational rollbacks. Based on my engineering experience, edge deployment often fails because:

- **Non-reproducible results**: performance depends on hardware, backend versions, parameters, and system load.
- **Opaque artifacts**: “optimized model” deliverables may not include sufficient evidence for internal review.
- **Weak auditability**: lack of integrity checks makes it hard to verify that “the evaluated artifact” equals “the shipped artifact.”
- **Rollback friction**: regressions are discovered late, with incomplete provenance.

### 1.2 Key idea
I designed UMC to treat an edge inference deliverable as an **auditable evidence bundle**. The bundle is the unit of trust: measurable claims must be backed by artifacts and reproducible steps, and releases are subject to audit gates.

### 1.3 Contributions
- **Evidence Pack format**: a minimal set of artifacts (`env/results/report/manifest`) that captures methodology, environment fingerprint, and integrity.
- **Audit gate**: automated checks that validate artifact completeness and block common leakage patterns.
- **Public baseline pack**: a baseline-measured reference release that demonstrates reproducibility and auditability without forward-looking claims.

---

## 2. Problem Statement: the Last-Mile Trust Gap

I formalize the trust gap as the mismatch between:

- What stakeholders need to approve deployment (reproducible metrics, known methodology, integrity, rollback plan), and
- What they often receive (a binary/model file with limited provenance).

### 2.1 Threat model (engineering-focused)
UMC does not aim to defend against a fully malicious actor with system-level access. Instead, it targets common operational risks:

- Accidental mixing of versions (backend commit changes, parameter drift)
- Artifact incompleteness (missing env or methodology)
- Integrity loss (artifact modified after evaluation)
- Unintended leakage (local paths, usernames, tokens, private links)

---

## 3. UMC Evidence Pack Design

### 3.1 Minimal artifacts
I define an Evidence Pack with:

- `env.json`: minimal environment fingerprint (OS, CPU class, memory tier, runtime versions)
- `results.json`: measured metrics and methodology fields
- `report.md`: a one-page human-readable summary, reproduction steps, and risk/rollback notes
- `manifest.json`: integrity manifest (SHA-256 of artifacts)

This pack is intentionally small so it can be produced repeatedly and shared internally.

### 3.2 Design principles
- **Evidence-first**: claims are limited to what artifacts cover.
- **Methodology consistency**: focus on stable measurement procedures over single-number “wins.”
- **Safety defaults**: no forward-looking claims; no inclusion of weights or private datasets.
- **Rollback-ready**: each release is a provenance anchor; regression response is part of the deliverable.

### 3.3 Integrity and traceability
`manifest.json` binds the bundle’s content to cryptographic hashes. Reviewers can verify that the evaluated pack is identical to the shipped pack.

---

## 4. Audit Gate and Release Workflow

UMC provides a lightweight release workflow:

1. Generate artifacts (`env/results/report/manifest`).
2. Run audit gate (validate schema, completeness, and forbidden content).
3. Produce a minimal share bundle for distribution.

### 4.1 Forbidden content checks
The audit gate scans for:

- secrets (API keys, tokens, private keys)
- absolute local paths and workstation identifiers
- personal identifiers (emails/phones) if configured
- unintended binaries or weights

(See `SW_PUBLIC/tools/check_no_forbidden_files.py` and `SW_PUBLIC/scripts/audit_public.ps1`.)

---

## 5. Evaluation

### 5.1 What I evaluate
I evaluate UMC as an engineering system:

- **Reproducibility**: can independent runs regenerate artifacts under the same procedure?
- **Auditability**: can a reviewer validate completeness and integrity quickly?
- **Operational readiness**: is rollback guidance included?

### 5.2 Public baseline-measured pack
This repository publishes a **baseline-measured** pack (GGUF / llama.cpp / Q2_K) with:

- cold start latency (p50/p95)
- peak RSS
- stability (long run minutes, crash count)

All numbers are sourced from `SW_PUBLIC/artifacts/results.json` and summarized in `SW_PUBLIC/artifacts/report.md`.

> **Important**: Candidate improvements (e.g., UMC L8/L16) are intentionally not claimed unless measured under the same methodology and included as artifacts.

### 5.3 Limitations of current public evaluation
- Single baseline configuration (extend to multiple backends and hardware tiers)
- Limited task diversity (extend beyond microbenchmarks)
- Candidate artifacts withheld from public pack (to avoid unverified claims)

---

## 6. Discussion: Compatibility with Decoupled Architectures

Many next-generation inference stacks increasingly separate **static knowledge storage** from **dynamic compute** (e.g., lookup-based memory blocks and a compute graph). UMC is designed as a *container + evidence* layer that can support:

- sharded storage with metadata
- integrity verification
- patch-style incremental updates

This section is exploratory and makes no performance claims; it motivates why an auditable container standard becomes more valuable as systems become more modular.

---

## 7. Related Work

(Placeholder — to be expanded)

- quantization formats and inference backends (GGUF, llama.cpp)
- reproducibility and ML systems measurement
- software supply chain integrity (SBOM, checksums)

---

## 8. Final Thoughts

My core thesis is that edge LLM deployment is primarily an evidence problem: if artifacts are reproducible, auditable, and rollback-ready, organizations can evaluate and ship with lower risk. This preprint releases a baseline-measured public pack and a strict audit gate, and invites community scrutiny of the methodology.

---

## Appendix A. Artifact Schemas (Pointers)

- `SW_PUBLIC/schemas/env.schema.json`
- `SW_PUBLIC/schemas/results.schema.json`
- `SW_PUBLIC/artifacts/manifest.json`

## Appendix B. Reproduction

See `SW_PUBLIC/REPRODUCE.md` and scripts under `SW_PUBLIC/scripts/`.

## Appendix C. Release and Audit

- `SW_PUBLIC/scripts/audit_public.ps1`
- `SW_PUBLIC/tools/validate_artifacts.py`
- `SW_PUBLIC/tools/check_no_forbidden_files.py`
