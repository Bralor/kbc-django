import json

from django.db import DatabaseError, IntegrityError
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from blog.models import Blog, BlogReview
from blog.forms import (CommentCreateForm,
                        BlogReviewForm,
                        BlogSearchForm,
                        BlogModelForm)


# === HTML views (classic Django application) ===
@require_http_methods(["GET"])
def blog_list(request: HttpRequest) -> HttpResponse:
    blogs = Blog.objects.all()
    return render(request,
                  'blog/blog_list_static_example.html',
                  {'blogs': blogs})


class BlogDetailView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        blog = get_object_or_404(Blog, id=id)
        return render(request, 'blog/detail_preview.html', {'blog': blog})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def blog_create(request: HttpRequest) -> HttpResponse:
    form = BlogModelForm(request.POST or None)  # TODO: Explain

    if form.is_valid():
        try:
            blog = form.save(commit=False)

            if not blog.slug:
                blog.slug = blog.title.lower().replace(' ', '-')
            blog.save()

        except (DatabaseError, IntegrityError):
            return render(request, 'blog/blog_form.html', {'form': form, 'error': 'Nepodařilo se uložit blog. Zkuste to znovu.'})
        return redirect('blog:blog_detail', id=blog.id)
    return render(request, 'blog/blog_form.html', {'form': form})


@csrf_exempt
def blog_update(request: HttpRequest, pk: int):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = BlogModelForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return render(request, 'blog/blog_update_success.html', {'form': form, 'blog': blog})
    else:
        form = BlogModelForm(instance=blog)  # pre-fill form with existing data

    return render(request, 'blog/blog_form.html', {'form': form, 'blog': blog})


@require_http_methods(["GET"])
def blog_search(request: HttpRequest) -> HttpResponse:
    form = BlogSearchForm(request.GET)
    blogs = []

    if form.is_valid():
        query = form.cleaned_data['q']
        sort = form.cleaned_data['sort']
        blogs = Blog.objects.all()

        if query:
            blogs = blogs.filter(title__icontains=query)
        blogs = blogs.order_by(sort)  # safe: sort je whitelisted přes ChoiceField
    return render(request, 'blog/search.html', {'form': form, 'blogs': blogs})


@require_http_methods(["GET", "POST"])
def comment_create(request: HttpRequest) -> HttpResponse:
    form = CommentCreateForm(request.POST or None)

    if form.is_valid():
        return render(request, 'blog/comment_success.html', {'data': form.cleaned_data})

    return render(request, 'blog/comment_form.html', {'form': form})


@require_http_methods(["GET", "POST"])
def review_create(request: HttpRequest) -> HttpResponse:
    form = BlogReviewForm(request.POST or None)
    if form.is_valid():
        BlogReview.objects.create(
            blog=form.cleaned_data['blog'],
            user_id=1,  # default user for demo purposes
            rating=form.cleaned_data['rating'],
            comment=form.cleaned_data['comment'],
        )
        return redirect('blog:review_form_success')

    return render(request, 'blog/review_form.html', {'form': form})


def review_success(request: HttpRequest) -> HttpResponse:   # TODO: Explain
    return render(request, 'blog/review_success.html')


# === JSON API views (REST-like přístup) ===
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_blog_list_create(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        blogs = list(
            Blog.objects.order_by('-id').values('id', 'title', 'author', 'published_date')
        )
        return JsonResponse({'count': len(blogs), 'results': blogs})

    data = json.loads(request.body)
    form = BlogModelForm(data)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    blog = form.save()
    return JsonResponse({'id': blog.id, 'title': blog.title}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def api_comment_create(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    form = CommentCreateForm(data)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'status': 'ok', 'data': form.cleaned_data}, status=201)
