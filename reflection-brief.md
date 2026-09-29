# Reflection Brief — Evaluation and Observability Capstone

**Name:** Syed Zafar Sohail Ahamed
**Date:** 2026-09-29

> Ground every answer in your own run. When a question asks for a number, file name, or line, paste
> it from your artifacts — a reviewer should be able to find it. Answers that are correct in the
> abstract but cite nothing do not meet the bar. Keep it short and specific.

---

## 0. Environment

| Field | Value |
|---|---|
| OS & version | Linux 6.6.137+ (x86_64) |
| Python version | Python 3.13.2 (`/opt/venv/bin/python`) |
| Date run | 2026-09-29 |
| Ran any system live? (which) | No. External live calls were blocked by API proxy authentication errors (401 invalid x-api-key); all systems were executed using the lab's deterministic test suites, fixture caching (`--mode replay`), and `--offline` evaluation modes. |

---

## 1. Validated, routed pipeline

| Evidence | Value |
|---|---|
| Passing test count | 45 passed, 3 skipped |
| Routing output file | `capstone-submission/01-policy-pipeline/routing_decisions.json` |
| auto_approve / human_review / spot_check counts | 1 / 2 / 1 |

**1a. Retry boundary.** From your perturbation run (a required field removed), paste the escalation
record. How many API calls did the system make, and why is retrying a futile case worse than
escalating it?

> `{"kind":"escalation","policy_id":"POL-EMPTY","field":"coverage_limit","reason":"missing required field","retries_used":1,"status":"retry_futile_escalation"}`
>
> The system aborted after 1 call rather than consuming the maximum retry budget. When a field is structurally missing from the source document, model retries repeatedly re-prompt on identical missing facts. Retrying a futile case burns tokens, increases latency, and risks hallucinations under pressure to fill a required field, whereas immediate escalation cleanly logs the defect and routes it to a human.

**1b. Reading the router.** Pick one `human_review` record from your routing output. Which of the
three signals (confidence, reviewer, integration) sent it to a human? If you had trusted the model's
confidence alone, what would have happened?

> In `capstone-submission/01-policy-pipeline/routing_decisions.json`, policy `POL-101` was sent to `human_review` because the field-level confidence for `premium_amount` was `0.65` (falling below the routing threshold of `0.90`), even though the independent reviewer and integration sanity checks passed without errors.
>
> If the router had relied solely on the model's aggregate output or overall confidence score (which was pulled high by `0.99` scores on all other fields), `POL-101` would have been erroneously auto-approved into downstream underwriting.

**1c. Where the aggregate lies.** Run the calibration snippet. Quote the one cell whose accuracy lags
its confidence, plus the overall figure. What does slicing by `policy_type × field` catch that a
single number hides?

> From `capstone-submission/01-policy-pipeline/calibration-report.txt`:
> ```text
> umbrella  exclusions      n=2 conf=0.93 acc=0.00 brier=0.865
> OVERALL brier=0.291
> ```
> Slicing by `policy_type × field` unmasks severe local miscalibration. While an aggregate Brier score of `0.291` across the suite appears reasonably healthy, the `umbrella / exclusions` slice was 93% confident while being 0% accurate (`brier=0.865`). Slicing prevents strong performance on common, simpler fields (like `auto / premium_amount` at `brier=0.003`) from masking total failure modes on complex legal exclusions.

---

## 2. Schema-enforced two-pass extraction

| Evidence | Value |
|---|---|
| Passing test count | 25 passed |
| Document run | `fixtures/documents/income_missing_bonus.txt` |
| Classified type | Single-borrower W-2 wage earner; extracted `base_monthly: 5673.08`, `stated_monthly_total: null` |

**2a. Two guarantees.** Paste your discrepancy-run output. Tool use already forces valid JSON, yet the
validator still catches a bad sum. Why are these two different guarantees? Name one error each cannot
catch.

> From `capstone-submission/02-mortgage-extraction/discrepancy-run.txt`:
> ```json
> "validation": {
>   "consistent": false,
>   "discrepancies": [
>     {
>       "field": "total_monthly_income",
>       "calculated": 9642.17,
>       "stated": 10892.17,
>       "delta": -1250.0
>     }
>   ]
> }
> ```
> Tool use enforces **syntactic integrity** (ensuring valid JSON syntax and conformant primitive data types), whereas deterministic validation enforces **semantic and arithmetic integrity**. Tool use cannot catch mathematical inconsistencies (e.g., component numbers summing to `9642.17` while the stated sum is `10892.17` in perfectly valid JSON). Conversely, mathematical validation cannot catch syntactic failures like malformed payloads or schema type mutations that break parsing before validation can execute.

**2b. Refusing to fabricate.** Run on a document missing a field. Paste that field's output. Why null
instead of an invented value? Point to the schema choice that allows it.

> From `capstone-submission/02-mortgage-extraction/extract-run.txt` (on `income_missing_bonus.txt`):
> ```json
> "bonus_monthly": null,
> "bonus_ytd": null,
> "stated_monthly_total": null
> ```
> The extractor returns `null` because the Pydantic model declares these attributes with optional types (e.g., `bonus_monthly: float | None = None`). By explicitly allowing nullable types in the schema contract, the model is guided to return an explicit `null` when a value is omitted from the source text instead of guessing or fabricating a value.

**2c. Normalization.** Quote one field where the source text and extracted value differ in format
("about 2,400 sq ft" → `2400`). Why normalize at extraction time rather than downstream?

> From `fixtures/documents/appraisal_informal_sqft.txt` running through the appraisal extractor: `"about 2,400 sq ft"` extracted into `"gross_living_area_sqft": 2400`.
>
> Normalizing during extraction converts fuzzy, human-entered text into strict numeric primitives immediately. This prevents every downstream calculation, comparison check, and database ingestion step from having to implement redundant, fragile regex parsers.

---

## 3. Multi-source synthesis

| Evidence | Value |
|---|---|
| Passing test count | 34 passed in 60.14s |
| Briefing file | `capstone-submission/03-supply-chain/briefing.txt` |
| Section the conflict landed in | `Contested` |

**3a. Annotate, don't arbitrate.** Quote one conflicting-metric pair from your briefing — both values,
sources, dates. Give one way a reader is better served by the preserved conflict than by a single
reconciled number.

> In `capstone-submission/03-supply-chain/briefing.txt`:
> `95.0% — supplier_audit (as of 2026-04-10)` vs `78.0% — logistics (as of 2026-04-05)` for `on_time_delivery_rate`.
>
> Preserving the conflict alerts risk officers to an active discrepancy between self-reported audit metrics and actual logistics sensor data. Averaging or arbitrating the two into an artificial `86.5%` would erase the signal that one source is either out-of-date or misrepresenting operational reality.

**3b. Source goes dark.** Run with `--simulate-timeout`. Paste the part of the briefing showing the
failed source. How is "unreachable" handled differently from "nothing to report," and why does the run
still finish?

> From `capstone-submission/03-supply-chain/timeout-run.txt`:
> ```text
> Sources unavailable: logistics unavailable (timeout)
> late_shipment_count: [missing source: timeout reading logistics]
> ```
> "Unreachable" is explicitly captured as an infrastructure degradation and logged in the `Incomplete` section. It is strictly differentiated from "nothing to report" (which indicates zero risk findings across reachable sources). The coordinator wraps each source call in a resilient timeout boundary, allowing partial synthesis across remaining sources without failing the entire run.

**3c. Dates as a guardrail.** Quote two claims about the same supplier with different dates. How does
requiring a date stop a time difference from reading as a contradiction?

> `supplier_audit (as of 2026-04-10)` vs `logistics (as of 2026-04-05)` for `on_time_delivery_rate`.
>
> Mandatory timestamp metadata establishes chronology: the 78% rate observed on April 5 and the 95% rate reported on April 10 represent sequential observations rather than a logical impossibility at a single instant in time.

---

## 4. Synthesis

**4a. One principle.** Name the single moment in your runs (system + artifact) where *evaluate the
output, don't trust the model's word* most clearly caught something a trusting design would have
shipped.

> In `capstone-submission/02-mortgage-extraction/discrepancy-run.txt`, the LLM output valid JSON containing stated income `10892.17`. A naive implementation would have accepted the JSON without issue, but the programmatic validator recalculated the itemized sum (`5416.67 + 1250.0 + 2140.0 + 385.5 + 450.0 = 9642.17`), flagging the `-1250.0` mismatch and preventing fraudulent financial data from entering the loan ledger.

**4b. Confidence ≠ correctness.** Pick the system where this mattered most, and explain why using
something you observed.

> In the policy extraction pipeline, the calibration report showed `umbrella / exclusions` scoring `conf=0.93` with `acc=0.00` (`brier=0.865`). Relying on model confidence would have auto-approved these umbrella policies, even though every single extraction in that category was completely incorrect.

**4c. Apply it.** Describe a real workflow where an LLM pulls structured results from messy input.
Which pattern — validated retry with escalation, independent review with deterministic routing, or
provenance-preserving conflict annotation — would you reach for first, and what would you instrument
to know when it broke?

> In an automated invoice-processing and accounts-payable workflow, I would reach for **validated retry with escalation** first.
>
> **Instrumentation:**
> 1. **Retry-to-Escalation Ratio:** Tracking how many retries succeed on the second attempt versus how many exhaust retries and escalate (detecting prompt drift or new vendor invoice layouts).
> 2. **Field-Level Validation Failure Rate:** Monitoring math mismatch rates across `subtotal + tax = total_due`.
> 3. **Per-Vendor Null Rates:** Measuring unexpected surges in `null` fields that identify when a supplier updates their document layout.