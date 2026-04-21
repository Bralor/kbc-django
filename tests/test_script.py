import pytest

from script import (validate_blog_post,
		    get_active_users,
		    get_unique_tags,
		    calculate_discount,
		    validate_author_name,
		    create_user_profile)


@pytest.mark.slow
def test_valid_post():
    result = validate_blog_post(
        title="Django Testing Guide",
        author="John Doe",
        content="This is a great blog post about Django testing."
    )
    assert result.is_valid == True
    assert result.errors == []


def test_author_with_numbers():
    result = validate_blog_post(title="My Post", author="John123", content="Clean content.")
    assert result.is_valid == False
    assert "Author must contain only letters and spaces" in result.errors


def test_author_with_special_chars():
    result = validate_blog_post(title="My Post", author="John@Doe", content="Clean content.")
    assert result.is_valid == False
    assert "Author must contain only letters and spaces" in result.errors


def test_no_spam_valid():
    result = validate_blog_post(
        title="My Post",
        author="John Doe",
        content="This is a great blog post about Django testing."
    )
    assert result.is_valid == True


def test_spam_content():
    result = validate_blog_post(title="My Post", author="John Doe", content="buy now!")
    assert result.is_valid == False
    assert "Content looks like spam" in result.errors


def test_multiple_errors():
    result = validate_blog_post(title="", author="John123", content="buy now!")
    assert result.is_valid == False
    assert len(result.errors) == 3


# Example test that will fail
def test_string_comparison():
    expected = "Hello, World!"
    actual = "Hello, world!"  # lowercase 'w'
    assert actual == expected


def test_string_patterns():
    message = "Order #12345 has been shipped"
    
    # Check substring
    assert "shipped" in message
    
    # Check prefix/suffix
    assert message.startswith("Order")
    assert message.endswith("shipped")
    
    # Check pattern exists
    assert "#" in message and message.split("#")[1].split()[0].isdigit()


def test_get_active_users():
    users = [
        {"username": "alice", "active": True},
        {"username": "bob", "active": False},
        {"username": "charlie", "active": True},
    ]
    
    result = get_active_users(users)
    
    #assert result == ["alice", "charlie"]
    assert result == ["charlie", "alice"]



def test_get_unique_tags():
    items = [
        {"name": "A", "tags": ["python", "django"]},
        {"name": "B", "tags": ["django", "api"]},
    ]
    
    result = get_unique_tags(items)
    
    # Order doesn't matter - compare as sets
    assert set(result) == {"python", "django", "api"}
    # Or check length + membership
    assert len(result) == 3
    assert "python" in result


def test_create_user_profile():
    profile = create_user_profile("john", "john@example.com")
    expected = {
        "username": "john",
        "email": "john@example.com",
        "status": "active",
        "role": "user",
    }
    assert profile == expected


def test_profile_has_required_fields():
    """Test that profile contains required fields (ignoring others)."""
    profile = create_user_profile("john", "john@example.com")
    
    # Check specific keys exist
    assert "username" in profile
    assert "email" in profile
    
    # Check specific values
    assert profile["username"] == "john"
    assert profile["status"] == "active"
    
    # Check subset of keys/values
    expected_subset = {"username": "john", "status": "active"}
    assert expected_subset.items() <= profile.items()


def test_discount_calculation():
    result = calculate_discount(100.0, 15.0)
    
    # Use pytest.approx for float comparison
    assert result == pytest.approx(85.0)


def test_floating_point_math():
    result = 0.1 + 0.2
    
    assert result == pytest.approx(0.3)


def test_approx_with_tolerance():
    """Specify custom tolerance."""
    result = 10.0
    
    # Relative tolerance (default is 1e-6)
    assert result == pytest.approx(10.001, rel=0.01)  # 1% tolerance
    
    # Absolute tolerance
    assert result == pytest.approx(10.001, abs=0.01)  # Within 0.01


def test_floating_point_naive():
    result = 0.1 + 0.2       # 0.30000000000000004
    assert result == 0.3    # FAILS!


def test_author_with_numbers_raises():
    """Test that author name with numbers raises ValueError."""
    with pytest.raises(ValueError):
        validate_author_name("John123")


def test_blog_post_has_title(sample_blog_post):
    """Test using the sample_blog_post fixture."""
    assert sample_blog_post["title"] == "My First Blog Post"
    assert sample_blog_post["author"] == "John Doe"


def test_blog_post_content_not_empty(sample_blog_post):
    """Another test using the same fixture."""
    assert len(sample_blog_post["content"]) > 0
