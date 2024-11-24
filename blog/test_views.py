from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import Post

class TestBlogViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.post = Post(title="Blog title", author=self.user,
                         slug="blog-title", excerpt="Blog excerpt",
                         content="Blog content", status=1)
        self.post.save()

    def test_render_post_detail_page_with_comment_form(self):
        response = self.client.get(reverse(
            'post_detail', args=['blog-title']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Blog title", response.content)
        self.assertIn(b"Blog content", response.content)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)

class TestPostListView(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser",
            password="password123",
            email="test@test.com"
        )
        self.post1 = Post.objects.create(
            title="Published Post",
            author=self.user,
            slug="published-post",
            excerpt="This is a published post.",
            content="Content of the published post.",
            status=1
        )
        self.post2 = Post.objects.create(
            title="Draft Post",
            author=self.user,
            slug="draft-post",
            excerpt="This is a draft post.",
            content="Content of the draft post.",
            status=0
        )

    def test_post_list_view_only_displays_published_posts(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Draft Post")

    def test_post_list_view_uses_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "blog/index.html")

class TestPostDetailView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.post = Post.objects.create(
            title="Sample Post",
            author=self.user,
            slug="sample-post",
            excerpt="This is a sample post.",
            content="Content of the sample post.",
            status=1
        )

    def test_post_detail_view_retrieves_correct_post(self):
        response = self.client.get(f"/post/{self.post.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Post")

    def test_post_detail_view_uses_correct_template(self):
        response = self.client.get(f"/post/{self.post.slug}/")
        self.assertTemplateUsed(response, "blog/post_detail.html")