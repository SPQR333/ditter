from social.forms import PostForm
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestSmokes(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        resp = self.client.get(reverse("social:index"))
        self.assertEqual(resp.status_code, 302)

    def test_register(self):
        resp = self.client.get(reverse("social:register"))
        self.assertEqual(resp.status_code, 200)


class TestPersonalPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        self.u.save()

    def test_personal_page(self):
        resp = self.client.get(reverse("social:user_detail", kwargs={"pk": self.u.id}))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.login(username="test", password="test")
        self.assertTrue(resp)

        resp = self.client.get(reverse("social:user_detail", kwargs={"pk": self.u.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.u.username)


class TestPostForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        self.u.save()

    def test_form(self):
        form_data = {"author": self.u.id, "title": "asdsadas", "content": "asdasdsad"}
        form = PostForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
