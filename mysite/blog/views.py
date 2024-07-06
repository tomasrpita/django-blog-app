from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

# from django.http import Http404
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
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

    SIMILAR_POST_MAX_COUNT = 4

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

    # List of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = (
        Post.published.filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(same_tags=Count("tags"))
        .order_by("-same_tags", "-publish")[:SIMILAR_POST_MAX_COUNT]
    )

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": commet_form,
            "similar_posts": similar_posts,
        },
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


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # search_vector = SearchVector("title", "body")
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(
                    # search=search_vector,
                    # rank=SearchRank(search_vector, search_query),
                    similarity=TrigramSimilarity("title", query),
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
            # results = (
            #     Post.published.annotate(
            #         search=search_vector,
            #         rank=SearchRank(search_vector, search_query),
            #     )
            #     # .filter(search=search_query)
            #     .filter(rank__gte=0.3)
            #     .order_by("-rank")
            # )
            # results = Post.published.annotate(
            #     search=SearchVector("title", "body"),
            # ).filter(search=query)
    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )
