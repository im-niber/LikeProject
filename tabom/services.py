from .models import Article, Like
from django.db.models import QuerySet
from django.db import transaction


@transaction.atomic
def do_like(user_id: int, article_id: int) -> Like:
    return Like.objects.create(user_id=user_id, article_id=article_id)


def undo_like(user_id: int, article_id: int) -> None:
    # 1
    """
    delete from tabom_like where user_id and article_id
    """
    Like.objects.filter(user_id=user_id, article_id=article_id).delete()

    # 2
    # like = Like.objects.filter(user_id=user_id, article_id=article_id).get()
    # like.delete()


def get_an_article(article_id: int) -> Article:
    return Article.objects.get(id=article_id)


def get_article_list(offset: int, limit: int) -> QuerySet[Article]:
    """
    DESC
    """
    return Article.objects.order_by("-id").prefetch_related("like_set")[offset : offset + limit]
