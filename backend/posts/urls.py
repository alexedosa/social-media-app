from django.urls import path
from .views import ListPost, CreatePost, PostDetail, CommentCreate

urlpatterns = [
    path('feed/', ListPost.as_view(), name='post-feed'),
    path('create/', CreatePost.as_view(), name='post-create'),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('comment/', CommentCreate.as_view(), name='post-comment'),
]
