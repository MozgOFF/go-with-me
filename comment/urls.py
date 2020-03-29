from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CommentListView, CreateCommentView

app_name = 'comment'
urlpatterns = [
    path('all', CommentListView.as_view()),
    path('create', CreateCommentView.as_view())
]
