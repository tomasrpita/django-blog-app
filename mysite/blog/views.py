from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
# from django.http import Http404

from .models import Post


def post_list(request):
    page_number = request.GET.get("page", 1)

    post_list = Post.published.all()
    paginator = Paginator(post_list, 5)
    posts = paginator.get_page(page_number)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("Post not found")
    post = get_object_or_404(
        # Post.published,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request, "blog/post/detail.html", {"post": post})
