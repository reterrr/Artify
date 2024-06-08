from django.urls import path
from .views import EventView, AddEventView

urlpatterns = [
    path('list', EventView.as_view()),
    path('create', AddEventView.as_view())
]
