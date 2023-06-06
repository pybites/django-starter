from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

from .models import Blog
from .forms import BlogForm


def blog_list(request):
    posts = Blog.objects.all()
    return render(request, 'blog/list.html', {'posts': posts})


def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})


def blog_new(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Added post')
        return redirect('blog:blog_list')
    else:
        messages.error(request, 'Could not add post')
    return render(request, 'blog/form.html', {'form': form})


def blog_edit(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    form = BlogForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Updated post')
        return redirect('blog:blog_list')

    return render(request, 'blog/form.html', {'post': post,
                                              'form': form})


def blog_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Deleted post')
        return redirect('blog:blog_list')

    return render(request, 'blog/delete.html', {'post': post})
