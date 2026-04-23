import pytest

from validators import validate_blog_post, validate_author_name


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


def test_simple_assert():
    assert 1 == 2


def test_author_with_numbers_raises():
    with pytest.raises(ValueError):
        validate_author_name("John123")
