import pytest


@pytest.fixture
def sample_blog_post() -> dict:
    """Provide a sample blog post for testing."""
    return {
        "title": "My First Blog Post",
        "author": "John Doe",
        "content": "This is a sample content for testing purposes only.",
    }


@pytest.fixture
def sample_comment() -> dict:
    """Provide a sample comment for testing."""
    return {
        "content": "Great post, very informative and well written!",
    }
