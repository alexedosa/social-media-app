from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Post, Comment
from .serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
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
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"msg": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"msg": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Security: Author check
        if post.author != request.user:
            return Response({"msg": "You do not have permission to edit this post"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostDetailSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"msg": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Security: Author check
        if post.author != request.user:
            return Response({"msg": "You do not have permission to delete this post"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"msg": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CommentCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
