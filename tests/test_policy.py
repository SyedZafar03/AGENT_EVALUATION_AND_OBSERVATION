def test_policy_routing_rules():
    routes = ["policy_check", "human_review", "auto_approve"]
    selected_route = "policy_check"
    assert selected_route in routes
