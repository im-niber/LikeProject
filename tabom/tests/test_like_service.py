from django.db import IntegrityError
from django.test import TestCase

from tabom.models import Article, User
from tabom.services import do_like


class TestLikeService(TestCase):

    def test_a_user_can_like_an_article(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test article")

        # When
        like = do_like(user.id, article.id)

        # Then
        self.assertIsNotNone(like)
        self.assertEqual(user.id, like.user.id)
        self.assertEqual(article.id, like.article.id)

    def test_a_user_can_like_an_article_only_once(self) -> None:
        #Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test article")

        # Expect
        like1 = do_like(user.id, article.id)
        with self.assertRaises(IntegrityError):
            like2 = do_like(user.id, article.id)

    def test_like_with_non_existing_user(self) -> None:
        # Given
        article = Article.objects.create(title="test article")

        # When
        with self.assertRaises(IntegrityError):
            like2 = do_like(12312412414, article.id)

        # Then

    def test_like_count_should_increase(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test article")

        # When
        do_like(user.id, article.id)

        # Then
        article = Article.objects.get(id=article.id)
        self.assertEqual(1, article.like_set.count())

