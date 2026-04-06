import json

from django.http import JsonResponse, HttpRequest, Http404, HttpResponse
from django.shortcuts import render
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Blog


def blog_list(request: HttpRequest):
    blogs = [blog for blog in Blog.objects.all()]
    return render(request, 'blog/blog_list_static_example.html', {'blogs': blogs})


class BlogDetailView(View):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        blog = get_object_or_404(Blog, id=id)

        return render(
            request,
            'blog/detail_preview.html',
            {'blog': blog},
        )


@csrf_exempt  # Only for demo/curl testing - in production use CSRF tokens
def blog_create(request):
    # Demo-only example: keep it intentionally minimal.
    if request.method != 'POST':
        return JsonResponse({'tip': 'Send POST with title, author, published_date'})

    data = json.loads(request.body)
    blog = Blog.objects.create(
        title=data['title'],
        author=data['author'],
        published_date=data['published_date'],
    )
    return JsonResponse({'id': blog.id, 'title': blog.title}, status=201)


def blog_search(request: HttpRequest) -> JsonResponse:    
    query = request.GET.get('q', '')          # 'django' or empty string
    sort = request.GET.get('sort', 'title')   # 'title' (default)
    blogs = Blog.objects.all()
    
    if query:
        blogs = blogs.filter(title__icontains=query)
    
    if sort in ('title', 'author', 'published_date'):
        blogs = blogs.order_by(sort)
    
    return JsonResponse(list(blogs.values()), safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def blog_list_create(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        blogs = list(
            Blog.objects.order_by('-id').values('id', 'title', 'author', 'published_date')
        )
        return JsonResponse({'count': len(blogs), 'results': blogs})

    if request.method == 'POST':
        data = json.loads(request.body)
        blog = Blog.objects.create(
            title=data['title'],
            author=data['author'],
            published_date=data['published_date'],
        )
        return JsonResponse({'id': blog.id, 'title': blog.title}, status=201)