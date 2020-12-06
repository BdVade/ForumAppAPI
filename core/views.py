from django.shortcuts import render

from .models import Post, Comment
from .serializers import *
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.http import JsonResponse


# Create your views here.
class PostList(ListAPIView):
    """List all posts"""
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(APIView):

    def get_object(self, slug, id=id):
        try:
            return Post.objects.get(slug=slug, id=id)
        except Post.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def get(self, request, slug, id):
        queryset = self.get_object(slug=slug, id=id)
        serializer = PostDetailSerializer(queryset)
        return Response(serializer.data)

class CategoryList(ListAPIView):
    """List all posts in a Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(APIView):

    def get_object(self, slug, id=id):
        try:
            return Category.objects.get(slug=slug, id=id)
        except Category.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def get(self, request, slug, id):
        queryset = self.get_object(slug=slug, id=id)
        serializer = CategoryDetailSerializer(queryset)
        return Response(serializer.data)


@api_view(['POST'])
def post_create(request, ):
    serializer = PostCreateSerializer()
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data)


# class CommentCreateView(CreateAPIView):
#     serializer_class = CommentSerializer
@api_view(['POST'])
def comment_create(request, post, id):
    """end point to create a comment to a post. Accepts the email of the poster
        and the body of the comment returns a response of the submitted values.
        Accepted keys are 'email' and 'body'"""
    serializer = CommentCreateSerializer(data=request.data)
    parent = Post.objects.get(slug=post, id=id)
    if serializer.is_valid():
        serializer.save(post=parent)
        return Response(serializer.data)

@api_view(['POST'])
def reply_create(request, parent_id):
    """end point to create a reply to a comment. Accepts the email of the poster
    and the body of the comment returns a response of the submitted values.
    Accepted keys are 'email' and 'body'"""
    serializer = CommentCreateSerializer(data=request.data)
    replying = Comment.object.get(id=parent_id)
    if serializer.is_valid():
        serializer.save(replying=replying)
        return Response(serializer.data)


# def comment_update(request, comment_id):
#     try:
#         comment = Comment.objects.get(id=comment_id)
#     except Comment.DoesNotExist:
#         raise HTTP_404_NOT_FOUND
#     if request.user not in comment.upvotes.all():
#         serializer = CommentSerializer(comment, data=request.data, partial=True)
#         serializer.save()
#     else:
#         comment.upvotes.remove(request.user)
#     return JsonResponse(serializer.data)
