def test_supply_chain_investigation_trace():
    trace = {
        "step_1": "Supplier identified",
        "step_2": "Discrepancy detected",
        "verdict": "Flagged"
    }
    assert "step_1" in trace
    assert trace["verdict"] in ["Approved", "Flagged", "Under Review"]
