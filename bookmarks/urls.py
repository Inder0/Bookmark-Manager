from django.urls import path,include
from .views import *

app_name='bookmarks'

urlpatterns=[
    path('', BookmarkListView.as_view(), name='home'),
    path('add/', AddBookmarkView.as_view(), name='add-bookmark'),
    path("search/",search_bookmarks,name="search_bookmarks"),
    path("delete/<int:pk>/",delete_bookmark, name="delete_bookmark"),
    path("list/", bookmark_list, name="bookmark_list"),
]