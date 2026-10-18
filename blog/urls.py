
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.PostListView.as_view(), name="home"),

    # Create a new post
    path(
        "post/create/",
        views.PostCreateView.as_view(),
        name="post_create",
    ),

    # My Posts
    path(
        "my-posts/",
        views.MyPostsView.as_view(),
        name="my_posts",
    ),

    # Post detail
    path(
        "posts/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),

    # Edit
    path(
        "posts/<slug:slug>/edit/",
        views.PostUpdateView.as_view(),
        name="post_update",
    ),

    # Delete
    path(
        "posts/<slug:slug>/delete/",
        views.PostDeleteView.as_view(),
        name="post_delete",
    ),

    # About
    path("about/", views.about, name="about"),

    # Contact
    path("contact/", views.contact, name="contact"),

    # Register
    path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),
]
