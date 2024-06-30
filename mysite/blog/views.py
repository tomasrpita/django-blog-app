from django.shortcuts import render, get_object_or_404
# from django.http import Http404

from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, id):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("Post not found")
    post = get_object_or_404(Post.published, id=id)
    return render(request, "blog/post/detail.html", {"post": post})