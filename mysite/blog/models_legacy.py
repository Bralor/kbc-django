# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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


class LegacyLegacyBlogReview(models.Model):
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
