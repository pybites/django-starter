from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect

from .models import Blog
from .forms import BlogForm


def blog_list(request):
    blog_list = Blog.objects.all()
    context = {'blog_list': blog_list}
    return render(request, 'blog/list.html', context)


def blog_detail(request, pk):
    context = {}
    context["data"] = Blog.objects.get(id=pk)

    return render(request, "blog/detail.html", context)


def blog_new(request):
    context = {}

    form = BlogForm(request.POST or None)
    if form.is_valid():
        form.save()

    context['form'] = form

    if request.method == "POST":
        return HttpResponseRedirect("/")

    return render(request, 'blog/create_view.html', context)


def blog_edit(request, pk):
    context = {}

    obj = get_object_or_404(Blog, id=pk)
    form = BlogForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()

    context["form"] = form

    if request.method == "POST":
        return HttpResponseRedirect("/")

    return render(request, 'blog/create_view.html', {'post': obj,
                                                     'form': form})

def blog_delete(request, pk):
    Blog.objects.filter(id=pk).delete()
    return redirect('/')
