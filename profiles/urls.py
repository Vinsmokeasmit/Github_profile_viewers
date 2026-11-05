from django.urls import path
from . import views


urlpatterns = [
    path("", views.jsearch, name="jsearch"),

    path(
        "bookmark/<str:username>/",
        views.bookmark,
        name="bookmark",
    ),

    path(
        "bookmarks/",
        views.bookmark_list,
        name="bookmarks",
    ),

    path(
        "bookmarks/<int:pk>/delete/",
        views.bookmark_delete,
        name="bookmark_delete",
    ),
    path('visualize/', views.visualize, name='visualize'),
    path("api/",views.search, name="search"),
]