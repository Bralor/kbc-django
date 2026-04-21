# blog/validators.py — reusable validators for Blog / Comment

from django.core.exceptions import ValidationError
import re


def validate_only_letters_and_spaces(value: str) -> None:
    """Allow only letters and spaces (used for Blog.author)."""

    if not re.match(r'^[a-zA-Z ]+$', value):
        raise ValidationError(
            "Only letters and spaces are allowed.",
            code='invalid_characters',
        )


def validate_no_spam_words(value: str) -> None:
    spam_words = ('buy now', 'click here', 'free money')

    for word in spam_words:
        if word in value.lower():
            raise ValidationError(
                "This content looks like spam and cannot be submitted.",
                code='spam',
            )


from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible  # required if used in model field validators (migrations)
class MinWordCountValidator:
    """Validate that a text field contains at least min_words words.

    Used for:
      - Blog.content  (long-form body, should be substantial)
      - Comment.content (should be more than one word)
    """

    def __init__(self, min_words: int = 10):
        self.min_words = min_words

    def __call__(self, value: str):
        word_count = len(value.split())
        if word_count < self.min_words:
            raise ValidationError(
                f"Please write at least {self.min_words} words. "
                f"Current count: {word_count}."
            )

    def __eq__(self, other):
        return (
            isinstance(other, MinWordCountValidator)
            and self.min_words == other.min_words
        )