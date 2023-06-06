import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from blog.models import Blog

@pytest.fixture
def blog(db):
    return Blog.objects.create(title='Test Blog',
                               post='Test Content',
                               slug='test-blog',
                               cover='https://example.com/cover.jpg')


def test_blog_list_view(client, blog):
    response = client.get(reverse('blog:blog_list'))
    assert response.status_code == 200
    assert list(response.context['posts']) == [blog]


def test_blog_detail_view(client, blog):
    response = client.get(reverse('blog:blog_detail', args=[blog.pk]))
    assert response.status_code == 200
    assert response.context['post'] == blog


def test_blog_new_view(db, client):
    data = {
        'title': 'New Blog',
        'post': 'New Content',
        'slug': 'new-blog',
        'cover': 'https://example.com/cover.jpg',
    }
    response = client.post(reverse('blog:blog_new'), data)
    assert response.status_code == 302
    assert Blog.objects.filter(title='New Blog').exists()

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Added post'


def test_new_blog_fails(db, client):
    data = {
        'title': 'New Blog',
        'post': 'New Content',
    }
    response = client.post(reverse('blog:blog_new'), data)
    assert response.status_code == 200
    assert not Blog.objects.filter(title='New Blog').exists()

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Could not add post'


def test_blog_edit_view(client, blog):
    data = {
        'title': 'Updated Blog',
        'post': 'Updated Content',
        'slug': 'updated-blog',
        'cover': 'https://example.com/updated_cover.jpg',
    }
    response = client.post(reverse('blog:blog_edit', args=[blog.pk]), data)
    assert response.status_code == 302

    updated_blog = Blog.objects.get(pk=blog.pk)
    assert updated_blog.title == 'Updated Blog'
    assert updated_blog.post == 'Updated Content'
    assert updated_blog.slug == 'updated-blog'
    assert updated_blog.cover == 'https://example.com/updated_cover.jpg'

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Updated post'


def test_blog_delete_view(client, blog):
    response = client.post(reverse('blog:blog_delete', args=[blog.pk]))
    assert response.status_code == 302
    assert not Blog.objects.filter(pk=blog.pk).exists()

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Deleted post'


def test_blog_delete_for_non_existing_blog(client, blog):
    wrong_id = Blog.objects.count() + 1
    response = client.post(reverse('blog:blog_delete', args=[wrong_id]))
    assert response.status_code == 404
