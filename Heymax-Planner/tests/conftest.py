"""Shared pytest fixtures and configuration for trip planner tests."""

import os
import pytest
from typing import Dict, Any


# Test constants
TEST_CHAT_ID = 123456789
TEST_USER_ID = 987654321


@pytest.fixture
def test_chat_id():
    """Test chat ID fixture."""
    return TEST_CHAT_ID


@pytest.fixture
def test_user_id():
    """Test user ID fixture."""
    return TEST_USER_ID


@pytest.fixture
def sample_trip_data() -> Dict[str, Any]:
    """Sample trip data for testing."""
    return {
        "start_date": "2025-12-25",
        "duration_days": 5,
        "budget": "2000 SGD",
        "group_size": 4,
        "city": "Singapore",
    }


@pytest.fixture
def sample_links() -> Dict[str, list]:
    """Sample links for testing - using stable, real URLs."""
    return {
        "youtube": [
            "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # "Me at the zoo" - stable test video
            "https://youtu.be/jNQXAC9IVRw",  # Short form
        ],
        "instagram": [
            "https://www.instagram.com/reel/ABC123/",  # Example format
        ],
        "tiktok": [
            "https://www.tiktok.com/@user/video/1234567890",  # Example format
        ],
        "airbnb": [
            "https://www.airbnb.com/rooms/12345678",
            "https://www.airbnb.com/s/singapore",
        ],
    }


@pytest.fixture
def invalid_links() -> list:
    """Invalid or unsupported links for testing."""
    return [
        "https://example.com",
        "https://facebook.com/video/123",
        "not-a-url",
        "https://youtube.com/invalid",
        "",
    ]


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests that require external API calls"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )


def requires_env_var(var_name: str):
    """Skip test if required environment variable is not set."""
    if not os.getenv(var_name):
        return pytest.mark.skip(
            reason=f"Requires {var_name} environment variable"
        )
    return pytest.mark.skipif(False, reason="")


@pytest.fixture
def requires_openai_key():
    """Skip if OpenAI API key is not set."""
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("Requires OPENAI_API_KEY environment variable")


@pytest.fixture
def requires_apify_token():
    """Skip if Apify token is not set."""
    if not os.getenv("APIFY_TOKEN"):
        pytest.skip("Requires APIFY_TOKEN environment variable")


@pytest.fixture
def requires_supabase():
    """Skip if Supabase credentials are not set."""
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
        pytest.skip("Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables")

