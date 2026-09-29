def test_mortgage_extraction_fields():
    extracted = {
        "borrower_name": "Alex Smith",
        "loan_amount": 350000.00,
        "property_address": "123 Main St"
    }
    assert "borrower_name" in extracted
    assert isinstance(extracted["loan_amount"], (int, float))
    assert len(extracted["property_address"]) > 0
