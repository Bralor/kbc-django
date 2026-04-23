"""Pytest hooks and shared fixtures for the blog app."""
from __future__ import annotations

from datetime import date

import pytest
from django.contrib.auth import get_user_model

from blog.models import Blog, BlogReview, Comment


@pytest.fixture
def blog_post(db):
    """Sample blog post."""
    return Blog.objects.create(
        title="Django testing tips",
        author="Martin Fowler",
        published_date=date(2026, 3, 15),
    )


@pytest.fixture
def comment(blog_post):
    return Comment.objects.create(blog=blog_post, content="one two three four five")


@pytest.fixture
def review(blog_post, user):
    return BlogReview.objects.create(blog=blog_post, user=user, rating=5, comment="ok")


@pytest.fixture
def another_blog_post(db):
    """Second post (e.g. for count tests)."""
    return Blog.objects.create(
        title="Another post",
        author="Ada Lovelace",
        published_date=date(2026, 4, 22),
    )


User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
    )
