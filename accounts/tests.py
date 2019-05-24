from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile

class TestUser(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create(
            username="jason",
            email="jason@email.com",
        )
        self.user.set_password("fake_password")
        self.user.save()

    def test_user_fields(self):
        self.assertEqual(self.user.username, "jason")
        self.assertEqual(self.user.email, 'jason@email.com')
        self.assertFalse(self.user.password == "fake_password")
