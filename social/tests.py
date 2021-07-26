from social.forms import PostForm
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Followers


class TestSmokes(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = User.objects.create_user(
            username="test", email="test@mail.com", password="test"
        )
        self.u.save()
        self.client.login(username="test", password="test")

    def test_user_detail(self):
        resp = self.client.get(reverse("social:user_detail", kwargs={"pk": self.u.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed("social/user_detail.html")

    def test_index(self):
        resp = self.client.get(reverse("social:index"))
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.get(reverse("social:register"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed("social/register.html")


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


class TestFollow(TestCase):
    def setUp(self):
        self.client = Client()
        self.u1 = User.objects.create_user(
            username="test1", email="test1@mail.com", password="test1"
        )
        self.u1.save()
        self.u2 = User.objects.create_user(
            username="test2", email="test2@mail.com", password="test2"
        )
        self.u2.save()

    def test_follow(self):
        resp = self.client.login(username="test1", password="test1")
        self.assertTrue(resp)

        resp = self.client.post(reverse("social:follow", kwargs={"pk": self.u2.id}))
        self.assertEqual(resp.status_code, 302)

        resp = self.u1.following.all()
        self.assertNotEqual(len(resp), 0)

        resp = resp[0].user
        self.assertEqual(resp.username, "test2")

    def test_follow_to_self(self):
        resp = self.client.login(username="test1", password="test1")
        self.assertTrue(resp)

        resp = self.client.post(reverse("social:follow", kwargs={"pk": self.u1.id}))
        self.assertEqual(resp.status_code, 302)

        resp = self.u1.following.all()
        self.assertEqual(len(resp), 0)

    def test_follow_to_non_existent_user(self):
        resp = self.client.login(username="test1", password="test1")
        self.assertTrue(resp)

        resp = self.client.post(reverse("social:follow", kwargs={"pk": 155}))
        self.assertEqual(resp.status_code, 404)

    def test_follow_get_request(self):
        resp = self.client.login(username="test1", password="test1")
        self.assertTrue(resp)

        resp = self.client.get(reverse("social:follow", kwargs={"pk": self.u1.id}))
        self.assertRedirects(
            resp, reverse("social:user_detail", kwargs={"pk": self.u1.id})
        )


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
