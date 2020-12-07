from rest_framework import serializers
from .models import Post,Comment,Category,UpVote,DownVote
from accs.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["__all__"]


class DownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownVote
        fields = "__all__"


class UpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpVote
        fields = "__all__"



class PostCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',]


class PostListSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    category = CategorySerializer()
    class Meta:
        model = Post
        fields = ['title', 'author','id','slug','category']

class CategoryDetailSerializer(serializers.ModelSerializer):
    category_posts = PostListSerializer()
    class Meta:
        model = Category
        fields = ['name', 'description', 'category_posts']

class ReplySerializer(serializers.ModelSerializer):
    upvotes = UpVoteSerializer(many=True, read_only=True)
    downvotes = DownVoteSerializer(many=True, read_only=True)


    class Meta:
        model = Comment
        fields = ['id','email', 'body', 'created','upvotes','downvotes',]
        read_only_fields = ['created','id']




class CommentSerializer(serializers.ModelSerializer):
    upvotes = UpVoteSerializer(many=True, read_only=True)
    downvotes = DownVoteSerializer(many=True, read_only=True)
    replies = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id','email', 'body', 'created','upvotes','downvotes', 'replies']
        read_only_fields = ['created','id']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['email', 'body',]

# class ReplyCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         mo



class PostDetailSerializer(serializers.ModelSerializer):
    post_comments = CommentSerializer(many=True)
    category = CategorySerializer()
    upvotes = UpVoteSerializer(many=True, read_only=True)
    downvotes = DownVoteSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title','body','author','created','post_comments','id','category',
                  'upvotes','downvotes']
        read_only = ['created', 'id']


