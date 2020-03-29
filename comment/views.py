from django.shortcuts import render
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer, CreateCommentSerializer
from rest_framework.permissions import IsAuthenticated


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer
