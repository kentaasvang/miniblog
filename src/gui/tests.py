from django.test import (
    TestCase, 
    Client
)

from .models import Post


class PostTests(TestCase):

    TITLE="my title"
    BODY="this is my content"
    PUBLISHED=False

    def setUp(self):
        self.client = Client()

        Post.objects.create(
            title=self.TITLE,
            body=self.BODY,
            is_published=self.PUBLISHED,
            )

    def test_simple_db_get(self):
        post: Post = Post.objects.get(id=1)
        self.assertEqual(post.title, self.TITLE)
        self.assertEqual(post.body, self.BODY)
        self.assertEqual(post.is_published, self.PUBLISHED)

    def test_frontpage_displays_posts_title(self):
        response = self.client.get("/")

        self.assertContains(response, self.TITLE)