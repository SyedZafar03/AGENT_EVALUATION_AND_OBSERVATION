# Evidence Pack — Evaluation and Observability Capstone

**Author:** Syed Zafar Sohail Ahamed  
**Date:** 2026-09-29  

This repository contains the evaluation, testing, and observability artifacts for three LLM-powered production pipelines developed as part of the **Claude AI Engineer Evaluation and Observability** capstone project.

---

## 1. Project Overview & Architecture

The three reference systems originate from the course repository (`cd15552 Claude AI Engineer Evaluation and Observability`). Each project is run from the `solution/` directory of its final exercise and installed into the environment with editable mode (`pip install -e ".[dev]"`), exposing its CLI tool directly on the system `$PATH`.

| Evidence Folder | Course Project & Final Exercise | Console Command | Core Architectural Patterns |
|---|---|---|---|
| `01-policy-pipeline/` | `Build a Validated, Routed Insurance Policy Extraction Pipeline/04-hitl-routing/solution/` | `policy-extractor` | Two-pass extraction, field-level confidence calibration, deterministic Human-in-the-Loop (HITL) routing, futile retry boundaries |
| `02-mortgage-extraction/` | `Build a Resilient Mortgage Document Extraction System/04-validate-mathematical-consistency/solution/` | `mortgage-extract` | Tool-enforced JSON syntax, deterministic mathematical validation, schema nullability contracts (refusal to hallucinate missing fields), extraction-time unit normalization |
| `03-supply-chain/` | `Investigate Supply Chain Risk with Multi-Source Synthesis/03-resilient-coordinator/solution/` | `supply-chain-investigate` | Multi-source risk synthesis, provenance-preserving conflict annotation (Annotate, don't arbitrate), resilient coordinator boundaries, partial degradation under source timeouts |

---

## 2. Evidence Pack Directory Layout

All evaluation traces, execution logs, test outputs, and generated synthesis reports are located inside the `capstone-submission/` directory:

capstone-submission/
├── reflection-brief.md            # Completed reflection brief citing exact empirical numbers and run artifacts
├── environment.txt                # System runtime specifications (Python version, host OS, virtual environment)
├── perturbation-log.md            # Documented perturbation failure experiments across all three systems
│
├── 01-policy-pipeline/
│   ├── tests.txt                  # Full pytest -v output (45 passed, 3 skipped)
│   ├── static-checks.txt          # Combined ruff check and mypy type validation output
│   ├── pipeline-run.txt           # Console output of policy-extractor pipeline data/policies/
│   ├── routing_decisions.json     # Generated routing decisions (auto_approve / human_review / spot_check)
│   ├── calibration-report.txt     # Sliced calibration report (policy_type × field Brier scoring)
│   └── screenshots/               # Terminal execution captures
│
├── 02-mortgage-extraction/
│   ├── tests.txt                  # Full pytest -v output (25 passed)
│   ├── static-checks.txt          # Combined ruff check and mypy type validation output
│   ├── extract-run.txt            # mortgage-extract output on standard income document
│   ├── discrepancy-run.txt        # Output demonstrating mathematical inconsistency detection
│   └── screenshots/               # Terminal execution captures
│
└── 03-supply-chain/
├── tests.txt                  # Full pytest -v output (34 passed)
├── static-checks.txt          # Combined ruff check and mypy type validation output
├── investigation-run.txt      # supply-chain-investigate meridian --offline output
├── briefing.txt               # Synthesized 3-section risk briefing (Verified, Contested, Incomplete)
├── timeout-run.txt            # Simulated source timeout demonstration (--simulate-timeout)
└── screenshots/               # Terminal execution captures


---

## 3. System Highlights & Verified Findings

### System 1: Validated, Routed Insurance Policy Pipeline
* **Passing Test Count:** 45 passed, 3 skipped.
* **Deterministic Routing Decisions:** Evaluated policies produced `1 auto_approve`, `2 human_review`, and `1 spot_check`.
* **Calibration & Slicing:** An overall Brier score of `0.291` hid a critical blind spot in the `umbrella / exclusions` slice (`conf=0.93`, `acc=0.00`, `brier=0.865`), demonstrating why confidence scores must be calibrated across categorical slices before determining routing thresholds.
* **Futile Retry Escalation:** When tested against an input with missing required fields (`coverage_limit`), the pipeline aborted after 1 call and escalated with status `retry_futile_escalation` rather than looping and consuming API budget on impossible extractions.

### System 2: Resilient Mortgage Extraction System
* **Passing Test Count:** 25 passed.
* **Dual-Layer Guarantee:** Demonstrated that while LLM tool use guarantees schema conformance and valid JSON syntax, it cannot ensure mathematical plausibility.
* **Discrepancy Catch:** In `discrepancy-run.txt`, the programmatic validator recalculated itemized earnings (`base: 5416.67 + bonus: 1250.0 + commission: 2140.0 + overtime: 385.5 + other: 450.0 = 9642.17`) and flagged a `-1250.0` mismatch against the stated total of `10892.17` (`"consistent": false`).
* **Refusal to Fabricate:** When run against `income_missing_bonus.txt`, the model respected nullable Pydantic field types (`bonus_monthly: float | None = None`), emitting explicit `null` values instead of inventing missing figures.

### System 3: Supply Chain Risk Multi-Source Synthesis
* **Passing Test Count:** 34 passed.
* **Annotate, Don't Arbitrate:** When conflicting on-time delivery rates were reported (`95.0%` from `supplier_audit` vs. `78.0%` from `logistics`), the coordinator preserved both timestamped claims under the `Contested` section rather than computing a misleading average.
* **Resilient Degradation:** Under `--simulate-timeout`, the coordinator captured the logistics failure as an unavailable source (`Incomplete` section) and successfully completed synthesis across remaining sources without crashing.

---

## 4. Environment & Execution Mode

* **Python Version:** 3.13.2 (`/opt/venv/bin/python`)
* **Operating System:** Linux 6.6.137+ (x86_64)
* **Execution Mode:** Because external live Anthropic API requests were intercepted by lab gateway authentication boundaries (401 invalid x-api-key), all three systems were evaluated deterministically using pre-recorded test fixtures (`--mode replay`), offline local vector indices (`--offline`), and reproducible pytest suites.

---

## 5. Artifact Inspection Reference

Reviewers can verify any metric or quote from `reflection-brief.md` directly in the underlying artifacts:
- **Calibration Scores:** `capstone-submission/01-policy-pipeline/calibration-report.txt`
- **Routing Decisions:** `capstone-submission/01-policy-pipeline/routing_decisions.json`
- **Arithmetic Delta Verification:** `capstone-submission/02-mortgage-extraction/discrepancy-run.txt`
- **Multi-Source Conflicts & Timeouts:** `capstone-submission/03-supply-chain/briefing.txt` and `timeout-run.txt`