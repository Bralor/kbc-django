from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    # === HTML views (classic Django application) ===
    path('', views.blog_list, name='blog_list'),
    path('<int:id>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('search/', views.blog_search, name='blog_search'),
    path('comment/create/', views.comment_create, name='comment_create'),
    path('review-form/', views.review_create, name='review_form'),
    path('review-form/success/', views.review_success, name='review_form_success'),

    # === JSON API views (REST-like approach) ===
    path('api/blogs/', views.api_blog_list_create, name='api_blog_list_create'),
    path('api/comments/', views.api_comment_create, name='api_comment_create'),
]