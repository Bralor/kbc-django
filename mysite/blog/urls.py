from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:id>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('search/', views.blog_search, name='blog_search'),
    path('list-create/', views.blog_list_create, name='blog_list_create'),
]