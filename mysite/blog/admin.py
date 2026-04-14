from django.contrib import admin
from blog.models import Blog, Comment, BlogReview


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at', 'updated_at')


class BlogReviewInline(admin.TabularInline):
    model = BlogReview
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category_type', 'published_date',)
    list_filter = ('category_type', 'published_date')
    search_fields = ('title', 'content', 'author')
    # list_editable = ('status',)
    list_per_page = 25
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    inlines = [CommentInline, BlogReviewInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'blog', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BlogReview)
class BlogReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'blog', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)


# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
