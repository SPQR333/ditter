from django.test import TestCase, Client
from django.urls import reverse


class TestSmokes(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        self.client.get(reverse("social:index"))


# class TestRegister(TestCase):
#     def
