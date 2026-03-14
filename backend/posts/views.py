from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Post, Comment
from .serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer
)

class PostPagination(PageNumberPagination):
    page_size = 5


class ListPost(APIView):
    def get(self, request):
        posts = Post.objects.all()
        paginator = PostPagination()
        paginated_posts = paginator.paginate_queryset(posts, request) 
        serializer = PostListSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)

class CreatePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Auto-assign the user here too!
            serializer.save(author=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetail(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostDetailSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"msg": "Post not found"}, status=404)


class Comment(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user) 
            return Response(serializer.data, status=201)
        