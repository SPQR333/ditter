from social.forms import PostForm
from unittest.suite import TestSuite
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages


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
        u = User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        u.save()

    def test_personal_page(self):
        resp = self.client.get(reverse("social:personal"))
        self.assertEqual(resp.status_code, 401)

        resp = self.client.login(username="test", password="test")
        self.assertTrue(resp)


class TestPostForm(TestCase):
    def setUp(self):
        self.client = Client()
        u = User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        u.save()

    def test_form(self):
        form_data = {"author": "1", "title": "asdsadas", "content": "asdasdsad"}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
