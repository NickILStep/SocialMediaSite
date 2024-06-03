from . import views
from django.urls import path

app_name = 'feed'
urlpatterns = [
    path('', views.index, name="index"),
    path('feed/', views.feed, name="feed"),
    path('post/<int:post_id>', views.postDetail, name="postDetail"),
    path('createPost/', views.CreatePost.as_view(), name="createPost"),
    path('updatePost/<int:post_id>', views.updatePost, name="updatePost"),
    path('deletePost/<int:post_id>', views.deletePost, name="deletePost"),
    path('comment/<int:comment_id>', views.commentDetail, name="commentDetail"),
    path('createComment/', views.CreateComment.as_view(), name="createComment"),
    path('createComment/<int:comment_id>', views.CreateComment.as_view(), name="createChildComment"),
    path('updateComment/<int:comment_id>', views.updateComment, name="updateComment"),
    path('deleteComment/<int:comment_id>', views.deleteComment, name="deleteComment"),
    path('savePost/<int:post_id>', views.savePost, name="savePost"),
    path('unsavePost/<int:post_id>', views.unsavePost, name="unsavePost"),
    path('likePost/<int:post_id>', views.likePost, name="likePost"),
    path('unlikePost/<int:post_id>', views.unlikePost, name="unlikePost"),
]