import secrets

RANDOM_STRING_CHARS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # noqa
)


async def get_random_string(
    length: int, allowed_chars=RANDOM_STRING_CHARS
) -> str:
    """Return a securely generated random string."""

    return "".join(secrets.choice(allowed_chars) for i in range(length))
