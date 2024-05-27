from django.urls import path
from .views import PostView, DeletePostView, FindPostView, UserCommentsView, PostCommentsView, PostLikesView, CreateLikeView

urlpatterns = [
    path('list', PostView.as_view()),
    path('create', PostView.as_view()),
    path('<int:pk>/delete', DeletePostView.as_view()),
    path('<int:pk>/get/', FindPostView.as_view()),
    path('user/<int:user_id>/comments', UserCommentsView.as_view()),
    path('post/<int:post_id>/comments', PostCommentsView.as_view()),
    path('post/<int:post_id>/likes', PostLikesView.as_view()),  
    path('like/create', CreateLikeView.as_view()),
]