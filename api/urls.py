from django.urls import path
from .views import news_entries_view

urlpatterns = [
    path('news/', news_entries_view, name='news_entries'),
]
