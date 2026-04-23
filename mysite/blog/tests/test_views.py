import pytest
from django.test import Client
from django.urls import reverse, resolve

from blog.models import Blog
from blog import views


@pytest.mark.django_db
def test_blog_list_returns_200(client):
    response = client.get(reverse("blog:blog_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_response_attributes(client):
    url = reverse("blog:blog_list")
    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/html")

    template_names = [t.name for t in response.templates]
    assert "blog/blog_list_static_example.html" in template_names

    assert b"blog" in response.content.lower()


@pytest.mark.django_db
def test_blog_list_shows_title(client, blog_post):
    url = reverse("blog:blog_list")
    response = client.get(url)

    assert blog_post.title.encode() in response.content
    assert blog_post.title in response.content.decode()


@pytest.mark.django_db
def test_blog_create_post(client):
    url = reverse("blog:blog_create")
    data = {
        "title": "My new blog",
        "author": "alice",
        "author_email": "",
        "content": "one two three four five",
        "published_date": "2026-03-01",
        "category_type": "1",
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert Blog.objects.filter(title="My new blog").exists()


@pytest.mark.django_db
def test_blog_create_redirects_to_detail(client):
    url = reverse("blog:blog_create")
    data = {
        "title": "Redirect me",
        "author": "bob",
        "author_email": "",
        "content": "alpha beta gamma delta",
        "published_date": "2026-02-01",
        "category_type": "1",
    }
    response = client.post(url, data)

    assert response.status_code == 302
    blog = Blog.objects.get(title="Redirect me")
    expected = reverse("blog:blog_detail", kwargs={"id": blog.id})
    assert response.url == expected


@pytest.mark.django_db
def test_blog_create_follow_redirect(client):
    url = reverse("blog:blog_create")
    data = {
        "title": "Follow redirect",
        "author": "carol",
        "author_email": "",
        "content": "one two three four words",
        "published_date": "2026-02-10",
        "category_type": "1",
    }
    response = client.post(url, data, follow=True)

    assert response.status_code == 200
    assert "Follow redirect".encode() in response.content


@pytest.mark.django_db
def test_csrf_enforced_on_comment_create():
    """Default test client skips CSRF; strict client matches browser behaviour."""
    url = reverse("blog:comment_create")
    data = {"content": "one two three four"}

    # No token: default Client() still reaches the view (often 200).
    assert Client().post(url, data).status_code == 200

    # No token + enforce_csrf_checks=True → 403 (comment_create is not @csrf_exempt).
    strict = Client(enforce_csrf_checks=True)
    assert strict.post(url, data).status_code == 403


@pytest.mark.django_db
def test_blog_detail(client, blog_post):
    # URL kwarg is `id`, not pk (see blog/urls.py).
    url = reverse("blog:blog_detail", kwargs={"id": blog_post.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert blog_post.title in response.content.decode()


def test_blog_list_url_resolves():
    resolver = resolve(reverse("blog:blog_list"))
    assert resolver.func == views.blog_list


def test_blog_detail_url_resolves():
    url = reverse("blog:blog_detail", kwargs={"id": 42})
    resolver = resolve(url)
    assert resolver.func.view_class == views.BlogDetailView
    assert resolver.kwargs["id"] == 42


@pytest.mark.django_db
def test_admin_index_for_superuser(client, admin_user):
    client.force_login(admin_user)
    response = client.get("/admin/")
    assert response.status_code == 200
