from django.http import JsonResponse, HttpRequest


def blog_list(request: HttpRequest):
    return JsonResponse({'message': 'Hello, World!'})