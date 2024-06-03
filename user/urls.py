from user.views import UserPostView, OwnUserDetailView, UserDetailByIdView, UserPostByIdView, UserEventsView, UserEventsByIdView
from django.urls import path

urlpatterns = [
    path('posts/', UserPostView.as_view(), name='user_posts'),
    path('posts/<int:user_id>/', UserPostByIdView.as_view(), name='public_user_posts'),
    path('info/', OwnUserDetailView.as_view(), name='user_info'),
    path('info/<int:user_id>/', UserDetailByIdView.as_view(), name='public-user-detail'),
    path('events/', UserEventsView.as_view(), name='user_events'),
    path('events/<int:user_id>/', UserEventsByIdView.as_view(), name='user-events-by-id')
]