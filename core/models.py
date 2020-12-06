from django.db import models
from django.utils.text import slugify
from shortuuidfield import ShortUUIDField
from accs.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

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

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    email = models.EmailField(blank=True)
    body = models.TextField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    created = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='user_upvotes',null=True, blank=True )
    downvotes = models.ManyToManyField(User, related_name='user_downvotes', null=True, blank=True )
    replying = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)

    class Meta:
        ordering = ('-created',)

