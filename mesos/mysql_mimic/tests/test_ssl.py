import os
from contextlib import closing
from ssl import PROTOCOL_TLS_SERVER
from ssl import SSLContext

import pytest
from tests.conftest import ConnectFixture
from tests.conftest import MockSession
from tests.conftest import query

CURRENT_DIR = os.path.dirname(__file__)
SSL_CERT = os.path.join(CURRENT_DIR, "fixtures/certificate.pem")
SSL_KEY = os.path.join(CURRENT_DIR, "fixtures/key.pem")


@pytest.fixture(autouse=True)
def ssl() -> SSLContext:
    sslcontext = SSLContext(PROTOCOL_TLS_SERVER)
    sslcontext.load_cert_chain(certfile=SSL_CERT, keyfile=SSL_KEY)
    return sslcontext


@pytest.mark.asyncio
@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="""
There seems to be a sequencing issue with the asyncio server starting tls.
https://stackoverflow.com/questions/74187508/sequencing-issue-when-upgrading-python-asyncio-connection-to-tls
Didn't have time to debug this, so skipping in CI for now.
""",
)
async def test_ssl(
    session: MockSession,
    connect: ConnectFixture,
    port: int,
) -> None:
    with closing(await connect()) as conn:
        results = await query(conn, "SELECT 1 AS a")
        assert results == [{"a": 1}]
