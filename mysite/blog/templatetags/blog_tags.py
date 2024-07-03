from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    total = Post.published.count()
    print("total_posts", total)
    return Post.published.count()
