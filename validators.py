
import re
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)


def is_valid_author(value: str) -> bool:
    return bool(re.match(r'^[a-zA-Z ]+$', value))


def has_no_spam_words(value: str) -> bool:
    spam_words = ('buy now', 'click here', 'free money')
    return not any(word in value.lower() for word in spam_words)


def validate_blog_post(title: str, author: str, content: str) -> ValidationResult:
    errors = []

    if not title:
        errors.append("Title is required")

    if not is_valid_author(author):
        errors.append("Author must contain only letters and spaces")

    if not has_no_spam_words(content):
        errors.append("Content looks like spam")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def validate_author_name(value: str) -> None:
    if not re.match(r'^[a-zA-Z ]+$', value):
        raise ValueError("Only letters and spaces are allowed.")
