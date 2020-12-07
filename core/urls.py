from django.urls import path
from .views import *
urlpatterns = [
    path('post/create/', post_create, name='post_create'),
    path('post/list/', PostList.as_view(), name='post_list' ),
    path('post/<slug:slug>/<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/upvote/',post_upvote, name='post_upvote'),
    path('post/<int:post_id>/downvote/',post_downvote, name='post_downvote'),
    path('categories/', CategoryList.as_view(),),
    path('categories/<slug:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('post/<slug:post>/<int:id>/comment/', comment_create, name="comment_create"),
    path('comment/<int:parent_id>/reply/', reply_create, name='reply_create'),
    path('comment/<int:comment_id>/upvote/',comment_upvote, name='comment_upvote'),
    path('comment/<int:comment_id>/downvote/', comment_downvote, name='comment_downvote'),

]