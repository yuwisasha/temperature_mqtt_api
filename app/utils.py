import secrets
import string
from ssl import SSLContext

from gmqtt import Client
from httpx import URL

from callbacks import assign_callbacks_to_client

RANDOM_STRING_CHARS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # noqa
)


async def get_random_string(
    length: int, allowed_chars=RANDOM_STRING_CHARS
) -> str:
    """Return a securely generated random string."""

    return "".join(secrets.choice(allowed_chars) for i in range(length))


async def get_client(
    broker_host: URL,
    broker_port: str,
    ssl_cntxt: SSLContext,
    username: str,
    password: str,
) -> Client:
    client = Client(
        await get_random_string(6, string.ascii_letters + string.digits)
    )
    assign_callbacks_to_client(client)
    client.set_auth_credentials(username, password)
    await client.connect(broker_host, broker_port, ssl=ssl_cntxt)

    return client
