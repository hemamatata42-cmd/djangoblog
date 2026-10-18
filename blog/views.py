from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q  # नयाँ फोटोको निर्देशन (लाइन ३१७२) अनुसार थपिएको इम्पोर्ट

from blog.forms import PostForm, RegisterForm
from .models import Post, Category


# Home page: Show published blog posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return (
            Post.objects
            .filter(status="published")
            .select_related("author", "category")
            .prefetch_related("tags")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


# Show one blog post (नयाँ फोटोको निर्देशन अनुसार ड्राफ्ट सुरक्षा मिलाइएको कोड)
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # सुरुमा प्रकाशित भएका पोस्टहरू मात्र फिल्टर गर्ने
        post = Post.objects.filter(status="published")
        
        # यदि प्रयोगकर्ता लगइन छ भने आफ्ना ड्राफ्ट पोस्टहरू पनि हेर्न दिने
        if self.request.user.is_authenticated:
            post = Post.objects.filter(
                Q(status="published") | Q(author=self.request.user)
            )
        return post


# Show posts created by the logged-in user
class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    context_object_name = "posts"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return (
            Post.objects
            .filter(author=self.request.user)
            .order_by("-created_at")
        )


# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            "Post published successfully!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


# Edit a post
class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


# Delete a post
class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().author == self.request.user


# Register a new user
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# About page
def about(request):
    return render(
        request,
        "blog/about.html",
        {"team": "DjangoBlog Team"}
    )


# Contact page
def contact(request):
    return render(request, "blog/contact.html")


# Custom 403 error page
def custom_403(request, exception=None):
    return render(
        request,
        "blog/403.html",
        status=403
    )
