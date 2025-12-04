import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_rate_limiting(client: AsyncClient):
    """
    Hit the login endpoint 6 times. 
    The limit is 5/minute.
    The 6th request MUST fail with 429.
    """
    # We don't even need valid credentials to trigger the rate limiter
    # The limiter runs BEFORE authentication logic
    form_data = {"username": "hacker@example.com", "password": "123"}

    # 1. Hit 5 times (Allowed)
    for i in range(5):
        response = await client.post("/auth/token", data=form_data)
        assert response.status_code != 429, f"Request {i+1} was blocked too early!"

    # 2. Hit 6th time (Blocked)
    response = await client.post("/auth/token", data=form_data)

    # 3. Assertions
    assert response.status_code == 429

    # FIX: Check for the specific string SlowAPI is returning
    # It returns something like: {"detail": "5 per 1 minute"}
    assert "5 per 1 minute" in response.text
