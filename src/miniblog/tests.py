from django.test import (
    TestCase, 
    Client
)
from django.contrib.auth.models import User
from .settings import SiteConfig


def _set_up_logged_in_superuser():
    client = Client()

    user = User.objects.create_superuser(
        username="admin", 
        email="admin@admin.admin",
        password="password"
        )

    client.force_login(user)

    return client


class AdminTests(TestCase):

    def setUp(self):
        self.client = _set_up_logged_in_superuser()

    def test_admin_site_displays_site_header(self):

        response = self.client.get("/admin/")
        self.assertContains(response, SiteConfig.SITE_HEADER)