from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ..models import Comment, Post

User = get_user_model()


class CommentModelTestCase(TestCase):
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
            approved_comment=False
        )

    def test_comment_post(self):
        self.assertEqual(self.post.id, self.comment.post.id)

    def test_comment_author(self):
        self.assertEqual(self.comment.author, self.user)

    def test_comment_text(self):
        self.assertTrue(self.comment.text == "This is comment text")

    def test_comment_created_date(self):
        import datetime
        self.assertEqual(
            type(self.comment.created_date),
            datetime.datetime
        )

    def test_comment_creation(self):
        self.assertTrue(
            isinstance(self.comment, Comment)
        )
        self.assertEqual(
            self.comment.__str__(),
            self.comment.text
        )

    def test_comment_approved_comment(self):
        self.assertEqual(
            self.comment.approved_comment,
            False
        )

    def test_comment_approve(self):
        self.comment.approve()
        self.assertEqual(
            self.comment.approved_comment,
            True
        )
