# Perturbation Log

## System 1: Insurance Policy Pipeline
- **Command:** `policy-extractor pipeline data/policies/ --mode replay`
- **Baseline:** Normal bundled policies processed cleanly through extraction and routing, producing:
  - `1 auto_approve`
  - `2 human_review`
  - `1 spot_check`
- **Perturbation command:** `policy-extractor pipeline data/policies_missing_coverage/ --mode replay` (or perturbed policy document `POL-EMPTY` with `coverage_limit` field removed).
- **Hypothesis:** The pipeline should recognize an unrecoverable structural omission, terminate retries immediately (after 1 attempt), and escalate rather than loop futilely or fabricate values.
- **Observed contrast:** `POL-EMPTY` escalated after `retries_used=1` with status `retry_futile_escalation` instead of producing a normal routed extraction. Logged escalation:
  `{"kind":"escalation","policy_id":"POL-EMPTY","field":"coverage_limit","reason":"missing required field","retries_used":1,"status":"retry_futile_escalation"}`

---

## System 2: Mortgage Document Extraction
- **Command:** `mortgage-extract fixtures/documents/income_standard.txt`
- **Baseline:** Valid paystub extractions verify arithmetic line-item calculations (`base + bonus + overtime + commission = total`), yielding `"consistent": true` with `discrepancies: []`.
- **Perturbation command:** `mortgage-extract fixtures/documents/income_discrepancy.txt` (or paystub fixture with stated total modified to `10892.17` while items sum to `9642.17`).
- **Hypothesis:** Pydantic schema validation will succeed syntactically, but mathematical validation will detect and flag the arithmetic discrepancy.
- **Observed contrast:** The model produced valid JSON, but the consistency validator caught the divergence, reporting `"consistent": false` with an exact delta of `-1250.0` (`calculated: 9642.17`, `stated: 10892.17`).

---

## System 3: Supply Chain Risk Synthesis
- **Command:** `supply-chain-investigate meridian --offline`
- **Baseline:** Normal investigation queries all configured data sources (`erp_system`, `logistics`, `supplier_audit`), generating a briefing where metrics are sorted into `Verified Claims` and `Contested Findings` with 0 missing sources.
- **Perturbation command:** `supply-chain-investigate meridian --offline --simulate-timeout`
- **Hypothesis:** Upstream logistics timeout will be isolated by resilient coordinator boundaries; unreachable sources will be flagged in `Incomplete`, and synthesis will succeed for reachable sources.
- **Observed contrast:** The investigation completed gracefully without process termination. Logistics was isolated and recorded under `Incomplete / Unavailable Data` (`Sources unavailable: logistics unavailable (timeout)` and `late_shipment_count: [missing source: timeout reading logistics]`), while remaining sources populated the briefing.
