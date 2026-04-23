from django.db import models
from django.contrib.auth.models import User


class CategoryType(models.IntegerChoices):
    TECH = 1, 'Technology'
    BUSINESS = 2, 'Business'
    LIFESTYLE = 3, 'Lifestyle'
    NEWS = 4, 'News'


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    published_date = models.DateField()

    # IntegerChoices example used in this lesson
    category_type = models.PositiveSmallIntegerField(
        choices=CategoryType.choices,
        default=CategoryType.TECH,
    )

    class Meta:
        ordering = ['-published_date', 'title']
        indexes = [
            models.Index(fields=['slug'], name='blog_blog_slug_d925e3_idx'),
            # Ascending only: mssql-django mishandles descending index columns
            # ('-published_date') during AlterField. Default ordering stays DESC above.
            models.Index(
                fields=['category_type', 'published_date'],
                name='blog_blog_categor_532e66_idx',
            ),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment on {self.blog.title}"


class BlogReview(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog_reviews'
        constraints = [
            models.UniqueConstraint(fields=['blog', 'user'], name='unique_blog_review'),
        ]
        indexes = [
            models.Index(
                fields=['blog', 'created_at'],
                name='blog_review_blog_id_98a2d8_idx',
            ),
        ]

    def __str__(self):
        return f"Review {self.rating}/5 for {self.blog.title}"