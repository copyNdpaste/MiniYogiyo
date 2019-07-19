from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.
def post_list(request):
    post_list = Post.objects.all()
    # published_date가 있는 경우에만 게시글 출력
    post_list = post_list.filter(published_date__lte=timezone.now())
    post_list = post_list.order_by('published_date')

    return render(request, 'blog/post_list.html', {
        'post_list': post_list,
    })


def post_detail(request, pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)   # 없는 페이지의 경우에 404에러가 뜬다.
    return render(request, 'blog/post_detail.html', {
        'post': post,
    })


def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_new(request):
    # request.POST, request.FILES

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():  # 유효성 검사
            post = form.save(commit=False)
            post.author = request.user  # 로그인 유저 정보 가져옴, 로그인 상태임을 인정받아야 함
            # post.published_date = timezone.now()  # 글 저장/ 수정시 글 게시 안되도록 주석처리
            post.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {
        'form': form
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        # 수정할 대상 넘겨줌
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {
        'form': form
    })


# 글 게시하기
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('post_list')


# 로그인 안한 사용자도 댓글 쓰기 가능
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
