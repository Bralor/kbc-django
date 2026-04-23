# Rebuild composite indexes without descending field names (mssql-django + AlterField).
# Safe for DBs created before 0002/0003 were adjusted; no-op if indexes already match.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="blog",
            name="blog_blog_categor_532e66_idx",
        ),
        migrations.AddIndex(
            model_name="blog",
            index=models.Index(
                fields=["category_type", "published_date"],
                name="blog_blog_categor_532e66_idx",
            ),
        ),
        migrations.RemoveIndex(
            model_name="blogreview",
            name="blog_review_blog_id_98a2d8_idx",
        ),
        migrations.AddIndex(
            model_name="blogreview",
            index=models.Index(
                fields=["blog", "created_at"],
                name="blog_review_blog_id_98a2d8_idx",
            ),
        ),
    ]
