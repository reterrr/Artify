from django.urls import path
from .views import PostView, DeletePostView, FindPostView, UserCommentsView, PostCommentsView, PostLikesView, CreateLikeView, CreatePostView, DeleteLikeView, LikeView, CommentView

urlpatterns = [
    path('list', PostView.as_view()),
    path('create', CreatePostView.as_view()),
    path('<int:pk>/delete', DeletePostView.as_view()),
    path('<int:pk>/get/', FindPostView.as_view()),
    path('user/<int:user_id>/comments', UserCommentsView.as_view()),
    path('post/<int:post_id>/comments', PostCommentsView.as_view()),
    path('post/<int:post_id>/likes', PostLikesView.as_view()),  
    path('like/create', CreateLikeView.as_view()),
    path('comment/create', CommentView.as_view()),
    path('like/<int:post_id>/<int:user_id>/delete', DeleteLikeView.as_view()),
    path('like/<int:post_id>/<int:user_id>/get', LikeView.as_view())
]