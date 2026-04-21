import re


def is_valid_author(value: str) -> bool:
    """Allow only letters and spaces (used for Blog.author)."""
    return bool(re.match(r'^[a-zA-Z ]+$', value))


def has_no_spam_words(value: str) -> bool:
    """Return False if content contains spam words."""
    spam_words = ('buy now', 'click here', 'free money')
    return not any(word in value.lower() for word in spam_words)


from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)


def validate_blog_post(title: str, author: str, content: str) -> ValidationResult:
    errors = []

    if not title:
        errors.append("Title is required")

    if not is_valid_author(author):
        errors.append("Author must contain only letters and spaces")

    if not has_no_spam_words(content):
        errors.append("Content looks like spam")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def get_active_users(users: list[dict]) -> list[str]:
    """Return usernames of active users."""
    return [u["username"] for u in users if u["active"]]


def get_unique_tags(items: list[dict]) -> list[str]:
    """Get unique tags from items (order not guaranteed)."""
    tags = set()
    for item in items:
        tags.update(item.get("tags", []))
    return list(tags)


def create_user_profile(username: str, email: str) -> dict:
    return {
        "username": username,
        "email": email,
        "status": "active",
        "role": "user",
    }


def calculate_discount(price: float, percent: float) -> float:
    return price * (1 - percent / 100)


def validate_author_name(value: str) -> None:
    """Allow only letters and spaces in author name."""
    if not re.match(r'^[a-zA-Z ]+$', value):
        raise ValueError("Only letters and spaces are allowed.")
