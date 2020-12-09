from django.shortcuts import render

from .models import Post, Comment, UpVote, Category
from .serializers import *
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework import status
from django.http import JsonResponse


# Create your views here.
class PostList(ListAPIView):
    """List all posts"""
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(GenericAPIView):

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
    """List all the Categories in the Forum"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(GenericAPIView):
    """Detail of a Category returns as response the name, description and posts takes the slug of the category as
    URL parameter"""

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug,)
        except Category.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    def get(self, request, slug,):
        queryset = self.get_object(slug=slug)
        serializer = CategoryDetailSerializer(queryset)
        return Response(serializer.data)


@api_view(['POST',])
def post_create(request, ):
    """End point to create post. Takes 'title', 'body', 'category' as parameter.Value of category
     should be the name of the category"""
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        cd = serializer.validated_data
        print(cd)
        category = cd["category"]
        # print(category)
        category = Category.objects.get(name=category)
        serializer.save(author=request.user,category=category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


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
    Accepted keys are 'email' and 'body'.path parameter *parent_id* is the id of the comment being replied to"""
    serializer = CommentCreateSerializer(data=request.data)
    replying = Comment.object.get(id=parent_id)
    if serializer.is_valid():
        serializer.save(replying=replying)
        return Response(serializer.data)


def comment_upvote(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise HTTP_404_NOT_FOUND
    try:
        com_upvote = UpVote.objects.get(user_upvotes=comment, voter=request.user)
        comment.upvotes.remove(com_upvote)
        comment.save()
        return JsonResponse({
            'status': True,
            'details': 'UpVote removed successfully',
            'upvote_count': comment.upvotes.count()
        })
    except UpVote.DoesNotExist:
        new_upvote = UpVote.objects.create(voter=request.user, )
        comment.upvotes.add(new_upvote)
        comment.save()
        new_upvote.save()
        return JsonResponse({
            'status': True,
            'details': 'UpVote added successfully',
            'upvote_count': comment.upvotes.count()
        })


def comment_downvote(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise HTTP_404_NOT_FOUND
    try:
        com_downvote = DownVote.objects.get(user_downvotes=comment, voter=request.user)
        comment.downvotes.remove(com_downvote)
        comment.save()
        return JsonResponse({
            'status': True,
            'details': 'DownVote removed successfully',
            'downvote_count': comment.downvotes.count()
        })
    except DownVote.DoesNotExist:
        new_downvote = DownVote.objects.create(voter=request.user, )
        comment.downvotes.add(new_downvote)
        comment.save()
        new_downvote.save()
        return JsonResponse({
            'status': True,
            'details': 'DownVote added successfully',
            'downvote_count': comment.downvotes.count()
        })


def post_upvote(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise HTTP_404_NOT_FOUND
    try:
        com_upvote = UpVote.objects.get(upvote_posts=post, voter=request.user)
        post.upvotes.remove(com_upvote)
        post.save()
        return JsonResponse({
            'status': True,
            'details': 'UpVote removed successfully',
            'upvote_count': post.upvotes.count()
        })
    except UpVote.DoesNotExist:
        new_upvote = UpVote.objects.create(voter=request.user, )
        post.upvotes.add(new_upvote)
        post.save()
        new_upvote.save()
        return JsonResponse({
            'status': True,
            'details': 'UpVote added successfully',
            'upvote_count': post.upvotes.count()
        })


def post_downvote(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise HTTP_404_NOT_FOUND
    try:
        post_downvote = DownVote.objects.get(downvote_posts=post, voter=request.user)
        post.downvotes.remove(post_downvote)
        post.save()
        return JsonResponse({
            'status': True,
            'details': 'DownVote removed successfully',
            'downvote_count': post.downvotes.count()
        })
    except DownVote.DoesNotExist:
        new_downvote = DownVote.objects.create(voter=request.user, )
        post.downvotes.add(new_downvote)
        post.save()
        new_downvote.save()
        return JsonResponse({
            'status': True,
            'details': 'DownVote added successfully',
            'downvote_count': post.downvotes.count()
        })
