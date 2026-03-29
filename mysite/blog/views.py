from django.http import JsonResponse, HttpRequest
from http import HTTPStatus
from blog.models import Blog


def blog_list(request: HttpRequest):
    blog_ids = [blog.id for blog in Blog.objects.all()]
    return JsonResponse(blog_ids, safe=False)


def blog_detail(request: HttpRequest, id: int):
    try:
        result = Blog.objects.get(id=id)
    
    except Blog.DoesNotExist:
        return JsonResponse(
            {'error': 'Blog not found'},
            status=HTTPStatus.NOT_FOUND,
        )
    return JsonResponse({
        'id': result.id,
        'title': result.title,
        'author': result.author,
        'published_date': result.published_date.isoformat()
    })