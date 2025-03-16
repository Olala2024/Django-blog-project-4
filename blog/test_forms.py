from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import Post


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

    def test_comment_form_valid(self):
        form_data = {
            "body": "This is a valid comment."
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {
            "body": ""  # Empty comment
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_submission_redirect(self):
        comment_data = {
            "body": "This is a valid comment."
        }
        response = self.client.post(f"/post/{self.post.slug}/", data=comment_data)
        self.assertRedirects(response, f"/post/{self.post.slug}/")

    def test_comment_form_submission_renders_post_detail(self):
        comment_data = {
            "body": ""  # Empty comment
        }
        response = self.client.post(f"/post/{self.post.slug}/", data=comment_data)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertContains(response, "This field is required.")