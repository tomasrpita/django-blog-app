from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

# from django.http import Http404
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post


def post_list(request, tag_slug=None):
    page_number = request.GET.get("page", 1)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = Post.published.filter(tags__in=[tag])
    else:
        post_list = Post.published.all()

    paginator = Paginator(post_list, 5)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


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

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    commet_form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "comment_form": commet_form},
    )


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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None

    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create Comment object but don't save to database yet
        comment = form.save(commit=False)
        print(comment.id)
        # Assign the current post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    return render(request, "blog/post/comment.html", {"post": post, "comment": comment})
