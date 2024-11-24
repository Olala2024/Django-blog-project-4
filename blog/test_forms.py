from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import Post
from .forms import CommentForm


class TestCommentSubmission(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.post = Post.objects.create(
            title="Post with Comments",
            author=self.user,
            slug="post-with-comments",
            content="Content for comments test.",
            status=1
        )
        self.client.login(username="testuser", password="password123")

    def test_valid_comment_submission(self):
        comment_data = {
            "body": "This is a valid comment."
        }
        response = self.client.post(f"/post/{self.post.slug}/", data=comment_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.post.comments.filter(body="This is a valid comment.").exists())

    def test_invalid_comment_submission(self):
        comment_data = {
            "body": ""  # Empty comment
        }
        response = self.client.post(f"/post/{self.post.slug}/", data=comment_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.post.comments.filter(body="").exists())