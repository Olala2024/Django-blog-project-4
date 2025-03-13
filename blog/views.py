from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post, Category
from .forms import CommentForm

class PostList(generic.ListView):
    template_name = "blog/index.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = Post.objects.filter(status=1).order_by('-created_on')
        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.category
        return context

def post_detail(request, slug):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        liked = True

    comment_form = CommentForm(request.POST)

    if request.method == "POST" and comment_form.is_valid(): 
        comment_form = CommentForm(data=request.POST)
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        messages.add_message(
            request, messages.SUCCESS,
            'Comment submitted and awaiting approval'
        )
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "liked": liked,
        },
    )

class PostLike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        # Toggle the like status for the logged-in user
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))