# Perturbation Log

## System 1: Insurance Policy Pipeline
- **Perturbation:** Removed the required `coverage_limit` field from test document `POL-EMPTY`.
- **Hypothesis:** The pipeline should recognize an unrecoverable structural omission, terminate retries immediately (after 1 attempt), and escalate to human review rather than burning API calls or guessing values.
- **Observed:** Escalated with record `{"kind":"escalation","policy_id":"POL-EMPTY","field":"coverage_limit","reason":"missing required field","retries_used":1,"status":"retry_futile_escalation"}`.

## System 2: Mortgage Extraction Pipeline
- **Perturbation:** Modified stated monthly income in test fixture to 10,892.17 while individual line items sum to 9,642.17.
- **Hypothesis:** Pydantic schema validation will succeed syntactically, but mathematical cross-validation will flag an arithmetic discrepancy.
- **Observed:** Programmatic validator returned `"consistent": false` with an exact delta of `-1250.0`.

## System 3: Supply Chain Risk Synthesis
- **Perturbation:** Executed offline synthesis with `--simulate-timeout` on the logistics source.
- **Hypothesis:** The coordinator will degrade gracefully: unavailable sources will be annotated under `Incomplete`, while remaining reachable sources synthesize successfully into `Verified` and `Contested`.
- **Observed:** Coordinator completed without crashing; logistics was logged under `Sources unavailable: logistics unavailable (timeout)` and `late_shipment_count: [missing source: timeout reading logistics]`.
