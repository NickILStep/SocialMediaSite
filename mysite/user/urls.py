from . import views
from django.urls import path
from . import views
from django.contrib.auth import views as authentication_views

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', authentication_views.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('logout/', authentication_views.LogoutView.as_view(template_name='user/logout.html'), name="logout"),
    path('profile/<username>', views.profilepage, name="profile"),
    path('editProfile/<username>', views.editProfile, name="editProfile"),
    path('followProfile/<profile_id>', views.followProfile, name="followProfile"),
    path('unfollowProfile/<profile_id>', views.unfollowProfile, name="unfollowProfile"),
    path('deleteUser/<username>', views.deleteUser, name="deleteUser"),
    path('savedPosts/<username>', views.savedPosts, name="savedPosts"),
    path('likedPosts/<username>', views.likedPosts, name="likedPosts"),
    path('followingPosts/<username>', views.followingPosts, name="followingPosts"),
    path('followers/<username>', views.followers, name="followers"),
]