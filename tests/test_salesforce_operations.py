from salesforce.salesforce_operations import authenticate_salesforce, query_productos_usados

def test_authenticate_salesforce():
    sf = authenticate_salesforce()
    assert sf is not None

def test_query_productos_usados():
    sf = authenticate_salesforce()
    if sf:
        records = query_productos_usados(sf, 2023)
        assert records is not None
        assert len(records) > 0


