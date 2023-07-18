import random

import factory
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from factory.django import DjangoModelFactory

from newsapp.models import Article, NewsSite, Submission, SubmissionDownvote, SubmissionUpvote
from treecomments.models import TreeComment


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")

    class Meta:
        model = User


class NewsSiteFactory(DjangoModelFactory):
    name = factory.Faker("company")
    description = factory.Faker("sentence")
    url = factory.Faker("url")
    rss_url = factory.Faker("url")

    class Meta:
        model = NewsSite


class ArticleFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    text = factory.Faker("paragraph", nb_sentences=10, variable_nb_sentences=True)
    url = factory.Faker("url")
    subtitle = factory.Faker("sentence")
    author = factory.Faker("name")
    pub_date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    image_url = factory.LazyFunction(
        lambda: f"https://picsum.photos/{random.randint(200, 400)}/{random.randint(200, 400)}"
    )
    image_caption = factory.Faker("sentence")
    news_site = factory.SubFactory(NewsSiteFactory)

    class Meta:
        model = Article


class SubmissionFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    text = factory.Faker("paragraph", nb_sentences=10, variable_nb_sentences=True)
    url = factory.Faker("url")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Submission


class SubmissionUpvoteFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)

    class Meta:
        model = SubmissionUpvote


class SubmissionDownvoteFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    submission = factory.SubFactory(SubmissionFactory)

    class Meta:
        model = SubmissionDownvote


class CommentFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    text = factory.Faker("paragraph", nb_sentences=10, variable_nb_sentences=True)
    created_on = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())

    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    object_pk = factory.SelfAttribute("content_object.id")
    site_id = 1

    class Meta:
        exclude = ["content_object"]
        abstract = True


class ArticleCommentFactory(CommentFactory):
    content_object = factory.SubFactory(ArticleFactory)
    parent = factory.SubFactory("newsapp._factories.ArticleCommentFactory")

    class Meta:
        model = TreeComment


class SubmissionCommentFactory(CommentFactory):
    content_object = factory.SubFactory(SubmissionFactory)
    parent = factory.SubFactory("newsapp._factories.SubmissionCommentFactory")

    class Meta:
        model = TreeComment
