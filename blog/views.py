from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Category, Comment
from .forms import CommentForm, ContactForm

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'blog/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        return render(request, 'blog/contact.html', {'form': form})

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

@method_decorator(login_required, name='dispatch')
class CommentUpdateView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        form = CommentForm(instance=comment)
        return render(request, 'blog/comment_edit.html', {'form': form})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('post_detail', slug=comment.post.slug)
        return render(request, 'blog/comment_edit.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CommentDeleteView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post_detail', slug=post_slug)