# Perturbation & Robustness Log

| Test Case | Modification / Perturbation | Expected Behavior | Observed Behavior | Status |
|:---|:---|:---|:---|:---|
| Policy Routing (REQ-002) | Rephrased clear exception using ambiguous colloquial wording | Escalate to human review | Routed to human_review | PASS |
| Mortgage Extraction (DOC-001) | Altered loan amount currency formatting (`$350,000` vs `350000.00`) | Normalize to float `350000.00` | Normalized correctly | PASS |
| Supply Chain Investigation | Swapped event log timestamp sequence | Reorder events by true timestamp | Handled reordered timestamps cleanly | PASS |
