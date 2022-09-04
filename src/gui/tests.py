from django.test import (
    TestCase, 
    Client
)

from faker import Faker

from .models import Post


def _posts_builder(num, is_published=True):
    faker = Faker()
    posts = []
    for _ in range(num):
        posts.append(
           Post(
               title=faker.text(10),
               body=faker.text(),
               is_published=is_published
           ) 
        )

    return posts

def _bulk_insert(data, obj):
    for datum in data:
        obj.objects.create(
            title=datum.title,
            body=datum.body,
            is_published=datum.is_published,
            )

class PostTests(TestCase):

    pub_posts = _posts_builder(10)
    not_pub_posts = _posts_builder(5, is_published=False)
    posts = pub_posts + not_pub_posts

    def setUp(self):
        self.client = Client()
        _bulk_insert(self.posts, Post)

    def test_simple_db_get(self):
        posts = Post.objects.all()
        self.assertEqual(len(posts), len(self.posts))



class GuiIndexViewTests(TestCase):

    pub_posts = _posts_builder(10)
    not_pub_posts = _posts_builder(5, is_published=False)
    posts = pub_posts + not_pub_posts

    def setUp(self):
        self.client = Client()
        _bulk_insert(self.posts, Post)

    def test_gui_index_view_shows_all_published_posts(self):
        response = self.client.get("/")

        for post in self.pub_posts:
            self.assertContains(response, post.title)

        self.assertEqual(
            len(response.context["posts"]), 
            len(self.pub_posts)
            )

    def test_gui_index_view_doesnt_show_unpublished_posts(self):
        response = self.client.get("/")

        for post in self.not_pub_posts:
            self.assertNotContains(response, post.title)


class PostView(TestCase):

    published_post = {
        "title": "my title", 
        "body": "this is the body",
        "is_published": True
        }

    unpublished_post = {
        "title": "my title", 
        "body": "this is the body",
        "is_published": False
        }
    
    # objects returned by Model.objects.create is stored here
    # because a reference to the Id is needed for testing
    # and an if-check using on existing id on PostModel 
    # prevents us from setting it ourself
    pub_post_id = None
    unpub_post_id = None
    
    def setUp(self):
        self.client = Client()

        created_pub_post = Post.objects.create(**self.published_post)
        created_unpub_post = Post.objects.create(**self.unpublished_post)

        self.pub_post_id = created_pub_post.id
        self.unpub_post_id = created_unpub_post.id

    def test_view_published_posts(self):
        response = self.client.get(f"/post/{self.pub_post_id}")
        self.assertContains(response, self.published_post["title"])

    def test_view_unpublished_posts(self):
        response = self.client.get(f"/post/{self.unpub_post_id}")
        self.assertEqual(response.status_code, 404)