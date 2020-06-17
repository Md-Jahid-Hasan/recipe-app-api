from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password="test1234"):
    """Create a sample user for test"""
    return get_user_model().objects.create_manager(email,password)


class TestModel(TestCase):
    def test_create_user_success(self):
        email = "recipe@gmail.com"
        passward = "testpass123"
        user = get_user_model().objects.create_manager(
            email=email,
            password=passward,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(passward))

    def test_user_email_normalize(self):
        """Test the user new email is Normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_manager(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_invalid_email_check(self):
        """Test a user give an invalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_manager(None, 'test123')

    def test_create_new_superuser(self):
        """Check that is the user is superUser"""
        user = get_user_model().objects.create_superuser(
            'test@Gmail.Com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Jahid",
        )
        self.assertEqual(str(tag), tag.name)
