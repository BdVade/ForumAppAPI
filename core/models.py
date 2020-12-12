from django.db import models
from django.utils.text import slugify
from shortuuidfield import ShortUUIDField
from accs.models import User
# from .serializers import UserDetailSerializer


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20,unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def post_count(self,):
        return self.category_posts.count

class UpVote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class DownVote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    upvotes = models.ManyToManyField(UpVote,"upvote_posts",null=True, blank=True , )
    downvotes = models.ManyToManyField(DownVote,"downvote_posts", null=True, blank=True )
    body = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    @property
    def upvotes_count(self):
        return self.upvotes.count

    @property
    def comments_count(self):
        return self.post_comments.count


    class Meta:
        ordering = ('-created',)

# queryset= User.objects.get(id=1)
class Comment(models.Model):
    email = models.EmailField(blank=True)
    body = models.TextField(max_length=1000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments',)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    created = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(UpVote, related_name='user_upvotes',null=True, blank=True )
    downvotes = models.ManyToManyField(DownVote, related_name='user_downvotes', null=True, blank=True )
    replying = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)

    class Meta:
        ordering = ('-created',)


