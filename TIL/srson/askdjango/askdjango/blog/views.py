from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.
def post_list(request):
    qs = Post.objects.all()

    search = request.GET.get('search')
    if search:
        qs = qs.filter(title__icontains=search)
    context = {
        'post_list': qs,
        'search': search,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)
