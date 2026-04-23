# blog/tests/test_models.py

import pytest
from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from blog.models import Blog, BlogReview


class TestBlogModel:
    @pytest.mark.parametrize(
        "field,expected",
        [
            pytest.param("str", "Django testing tips", id="str"),
            pytest.param("author", "Martin Fowler", id="author"),
            pytest.param("published_date", date(2026, 3, 15), id="published_date"),
        ],
    )
    def test_blog_post_has_expected_attributes(self, blog_post, field, expected):
        """One test function, several cases — ``@pytest.mark.parametrize``."""
        if field == "str":
            assert str(blog_post) == expected
        else:
            assert getattr(blog_post, field) == expected

    def test_title_max_length_enforced(self, db):
        """Very long titles fail model validation."""
        from django.core.exceptions import ValidationError

        post = Blog(
            title="x" * 201,
            author="Test",
            published_date=date(2026, 1, 1),
        )
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_multiple_posts(self, blog_post, another_blog_post):
        """Two fixtures yield two rows."""
        assert Blog.objects.count() == 2


class TestBlogReviewConstraints:
    def test_unique_review_per_user(self, blog_post, django_user_model):
        user = django_user_model.objects.create_user("u", "u@e.com", "pw")
        BlogReview.objects.create(blog=blog_post, user=user, rating=5)
        with pytest.raises(IntegrityError):
            BlogReview.objects.create(blog=blog_post, user=user, rating=3)

    def test_published_date_required(self, db):
        with pytest.raises(IntegrityError):
            Blog.objects.create(title="x", author="a", published_date=None)


class TestBlogReviewFieldValidation:
    def test_negative_rating_invalid(self, blog_post, django_user_model):
        user = django_user_model.objects.create_user("r", "r@e.com", "x")
        r = BlogReview(blog=blog_post, user=user, rating=-1, comment="nope")
        with pytest.raises(ValidationError):
            r.full_clean()

    @pytest.mark.parametrize("rating", [1, 2, 3, 4, 5])
    def test_rating_ok(self, blog_post, django_user_model, rating):
        user = django_user_model.objects.create_user(f"u{rating}", f"u{rating}@e.com", "x")
        r = BlogReview(blog=blog_post, user=user, rating=rating, comment="ok")
        r.full_clean()


class TestCascadeDelete:
    def test_delete_blog_removes_comments(self, blog_post, comment):
        cid = comment.pk
        from blog.models import Comment

        blog_post.delete()
        assert not Comment.objects.filter(pk=cid).exists()

    def test_delete_blog_removes_reviews(self, blog_post, review):
        rid = review.pk
        from blog.models import BlogReview

        blog_post.delete()
        assert not BlogReview.objects.filter(pk=rid).exists()

    def test_delete_user_removes_reviews_not_blog(self, blog_post, review):
        bid = blog_post.pk
        review.user.delete()
        from blog.models import Blog

        assert Blog.objects.filter(pk=bid).exists()