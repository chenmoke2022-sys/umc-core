# Trace: VLA Toy Experiment Design (AI-Assisted Thinking)

> **Context**: This document records the **decision-making process** behind the `vla_alignment_toy` example. It demonstrates how I used AI to decompose a complex research topic (VLA/Multimodal) into a verifiable engineering task.

## 1. Problem Decomposition (Tasking)

**Goal**: Demonstrate "Multimodal Alignment" capability without training a massive model (too expensive/slow for a demo).

**AI Trace / Reasoning**:
*   *Initial thought*: Fine-tune a LLaVA model? -> *Risk*: Requires GPU, large weights, complex env. Hard to reproduce in CI.
*   *Alternative*: Use pre-trained CLIP? -> *Risk*: Good for application, but doesn't prove "training/alignment" capability.
*   *Decision*: **Synthetic Toy**. Generate paired vectors (v, t) from a shared latent space. Train a projection head to recover the alignment.
    *   **Pro**: Runs on CPU. Zero weights. Pure code.
    *   **Con**: Not real data.
    *   **Mitigation**: Explicitly label it as a "Toy" for verifying the *training loop* and *ablation workflow*, not the model performance.

## 2. Experiment Design (Ablation)

**Goal**: Show ability to compare model architectures (Engineering/Research rigor).

**AI Trace / Reasoning**:
*   *Question*: What is the simplest structural change to test?
*   *Hypothesis*: A non-linear head (MLP) should align better than a linear head if the latent relationship is simple but noisy.
*   *Plan*:
    1.  **Baseline**: `LinearHead` (d_in -> d_proj).
    2.  **Candidate**: `MLPHead` (d_in -> hidden -> d_proj).
    3.  **Metric**: `retrieval@1` (Can we find the correct text pair for a given image in a batch?).

## 3. Metric Definition (Standardization)

**Goal**: Fix the evaluation surface so results are comparable.

**AI Trace / Reasoning**:
*   *Loss*: InfoNCE (Standard Contrastive Loss). Hard to interpret intuitively.
*   *Business Metric*: "Accuracy" of matching.
*   *Implementation*: In-batch retrieval. For batch size $N$, for each $v_i$, is $t_i$ the closest vector?
*   *Output Schema*: Need to log `loss_start`, `loss_end`, `at1_start`, `at1_end` for both heads.

## 4. Artifact Definition (Evidence)

**Goal**: What proves this ran successfully?

*   `env.json`: Prove it ran on local hardware (CPU).
*   `results.json`: The standard schema with numeric fields for both Linear and MLP metrics.
*   `report.md`: Auto-generated summary table (Markdown).

---

**Outcome**: The `examples/vla_alignment_toy` code was generated based on this blueprint.

