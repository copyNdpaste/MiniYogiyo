from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import (get_object_or_404,
                              redirect,
                              render,
                              )

from .forms import PostForm
from .models import Post


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title": "Post Form",
    }
    return render(request, "posts/post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, pk=id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:post_list")


def post_detail(request, id=None):
    instance = get_object_or_404(Post, pk=id)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "posts/post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "posts/post_list.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, pk=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "posts/post_form.html", context)
