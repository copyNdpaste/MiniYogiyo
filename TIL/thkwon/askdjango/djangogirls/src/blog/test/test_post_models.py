from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import Post, Comment

User = get_user_model()


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='thkwon',
            email='',
            password='hohoho123!',
            is_staff=True,
            is_superuser=True
        )

        self.post = Post.objects.create(
            author=self.user,
            title="This is title",
            text="This is text",
            created_date=timezone.now(),
        )

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text="This is comment text",
            created_date=timezone.now(),
            approved_comment=True
        )

    def test_post_author(self):
        self.assertEqual(self.post.author, self.user)

    def test_post_title(self):
        self.assertEqual(self.post.title, 'This is title')

    def test_post_text(self):
        self.assertTrue(self.post.text == "This is text")

    def test_created_date(self):
        import datetime
        self.assertEqual(
            type(self.post.created_date),
            datetime.datetime
        )

    def test_published_date(self):
        self.assertEqual(
            self.post.published_date,
            None
        )

    def test_post_creation(self):
        self.assertTrue(
            isinstance(self.post, Post)
        )
        self.assertEqual(
            self.post.__str__(),
            self.post.title
        )

    def test_post_publish(self):
        self.assertNotEqual(self.post.publish(), "")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            '/{post_id}/'.format(post_id=self.post.id)
        )

    def test_approved_comment(self):
        self.assertEqual(
            self.post.approved_comments().count(),
            1
        )
