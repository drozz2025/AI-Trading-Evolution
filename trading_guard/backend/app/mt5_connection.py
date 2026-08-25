from dataclasses import dataclass

@dataclass(frozen=True)
class MT5ConnectionRequest:
    account_id: str
    broker: str
    server: str

@dataclass(frozen=True)
class ConnectionStatus:
    account_id: str
    status: str
    read_only: bool


def begin_read_only_connection(request: MT5ConnectionRequest) -> ConnectionStatus:
    """Create the application-side state for an MT5 read-only connection.

    Actual broker authentication is delegated to the configured MT5 cloud provider.
    No MT5 password is accepted or persisted by this endpoint.
    """
    return ConnectionStatus(
        account_id=request.account_id,
        status="pending_provider_setup",
        read_only=True,
    )
