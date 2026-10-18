from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # पासवर्ड रिसेटका लागि यो इम्पोर्ट थपिएको हो
from blog import views

urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),

    # Home page
    path('', views.PostListView.as_view(), name='home'),

    # Create a new post
    path(
        'post/create/',
        views.PostCreateView.as_view(),
        name='post_create',
    ),

    # My posts
    path(
        'my-posts/',
        views.MyPostsView.as_view(),
        name='my_posts',
    ),

    # Post detail page
    path(
        'post/<slug:slug>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),

    # Edit a post
    path(
        'post/<slug:slug>/edit/',
        views.PostUpdateView.as_view(),
        name='post_update',
    ),

    # Delete a post
    path(
        'post/<slug:slug>/delete/',
        views.PostDeleteView.as_view(),
        name='post_delete',
    ),

    # Login and logout
    path(
        'accounts/',
        include('django.contrib.auth.urls'),
    ),

    # Register a new user
    path(
        'accounts/register/',
        views.RegisterView.as_view(),
        name='register',
    ),

    # About page
    path('about/', views.about, name='about'),

    # Contact page
    path('contact/', views.contact, name='contact'),
]

# फोटोको स्टेप २ (लाइन ३०८८) को निर्देशन अनुसार थपिएका ४ वटा पासवर्ड रिसेट URL हरू
urlpatterns += [
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="blog/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="blog/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="blog/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="blog/password_reset_complete.html"), name="password_reset_complete"),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

handler403 = 'blog.views.custom_403'
