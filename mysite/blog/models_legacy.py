from django.db import models
from django.contrib.auth.models import User


class LegacyBlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    author_email = models.CharField(max_length=254)
    category_type = models.SmallIntegerField()
    content = models.TextField()
    slug = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'blog_blog'


class LegacyComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    blog = models.ForeignKey(LegacyBlog, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'blog_comment'


class LegacyBlogReviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField()
    blog = models.ForeignKey(LegacyBlog, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'blog_reviews'
        unique_together = (('blog', 'user'),)
