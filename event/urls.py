from django.urls import path
from .views import EventView, AddEventView, DeleteEventView

urlpatterns = [
    path('list', EventView.as_view()),
    path('create', AddEventView.as_view()),
    path('<int:pk>/delete', DeleteEventView.as_view()),
]
