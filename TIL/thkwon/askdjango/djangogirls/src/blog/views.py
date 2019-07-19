from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    HttpResponseRedirect,
    redirect,
    render,
)
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Comment, Post


@login_required
def comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.approve()
    return redirect('blog:post_detail', post_id=comment.post.id)


@login_required
def comment_new(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', post_id=post.post_id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_new.html', {'form': form})


@login_required
def comment_remove(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('blog:post_detail', post_id=comment.post.id)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True
    ).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'object': post,
        'form': form
    }
    return render(request, 'blog/post_edit.html', context)


def post_list(request):
    published_post = Post.objects.filter(published_date__lte=timezone.now())
    sorted_published_post = published_post.order_by('published_date')

    return render(request, 'blog/post_list.html', {
        'posts_list': sorted_published_post,
    })


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_publish(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.publish()
    return redirect('blog:post_detail', post_id=post.id)


@login_required
def post_remove(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('blog:post_list')
