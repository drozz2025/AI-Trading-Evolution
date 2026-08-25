import pytest
from app.mt5_provider import MetaApiProvider

@pytest.mark.asyncio
async def test_metaapi_transport_requires_configuration():
    with pytest.raises(NotImplementedError):
        await MetaApiProvider().get_account("demo")
