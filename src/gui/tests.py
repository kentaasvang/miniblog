from django.test import (
    TestCase, 
    Client
)

from faker import Faker

from .models import Post



class PostTests(TestCase):

    faker = Faker()

    pub_posts = []
    not_pub_posts = []

    for _ in range(10):
        pub_posts.append(
           Post(
               title=faker.text(10),
               body=faker.text(),
               is_published=True
           ) 
        )

    for _ in range(5):
        not_pub_posts.append(
           Post(
               title=faker.text(10),
               body=faker.text(),
               is_published=False
           ) 
        )

    posts = pub_posts + not_pub_posts

    def setUp(self):
        self.client = Client()

        for post in self.posts:
            Post.objects.create(
                title=post.title,
                body=post.body,
                is_published=post.is_published,
                )

    def test_simple_db_get(self):
        posts = Post.objects.all()
        self.assertEqual(len(posts), len(self.posts))

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