from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>', views.blog_detail, name='blog_detail'),
    path('new', views.blog_new, name='blog_new'),
    path('edit/<int:pk>', views.blog_edit, name='blog_edit'),
    path('delete/<int:pk>', views.blog_delete, name='blog_delete'),
]
