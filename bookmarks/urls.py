from django.urls import path,include
from .views import *

app_name='bookmarks'

urlpatterns=[
    path('', BookmarkListView.as_view(), name='home'),
    path('add/', AddBookmarkView.as_view(), name='add-bookmark'),
]