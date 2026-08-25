from app.mt5_connection import MT5ConnectionRequest, begin_read_only_connection

def test_connection_is_read_only():
    result = begin_read_only_connection(MT5ConnectionRequest("demo", "Example Broker", "Demo-Server"))
    assert result.read_only is True
    assert result.status == "pending_provider_setup"
