from django.urls import path
from .views import user_detail,UserList

urlpatterns =[
    path('profile/<int:id>/', user_detail),
    # path('profile/<int:id>/', profile_edit),
    path('name-list/',UserList.as_view())

]