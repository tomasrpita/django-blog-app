from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

# from django.http import Http404
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


def post_list(request):
    page_number = request.GET.get("page", 1)

    post_list = Post.published.all()
    paginator = Paginator(post_list, 5)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("Post not found")
    post = get_object_or_404(
        Post.published,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request, "blog/post/detail.html", {"post": post})


class PostListView(ListView):
    """
    Alternative implementation of the post_list view using Django's generic class-based views.
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/post/list.html"


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, from_email=None, recipient_list=[cd["to"]])
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
