from django.shortcuts import render
from .serializers import UserDetailSerializer,ProfileEditSerializer,UserListSerializer
from .models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.generics import ListAPIView
# Create your views here.

@api_view(['GET'])
def user_detail(request, id):
    qs = User.objects.get(pk=id)
    serializer = UserDetailSerializer(qs)
    return JsonResponse(serializer.data)


@api_view(['PUT'])
def profile_edit(request,id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise HTTP_404_NOT_FOUND
    serializer = ProfileEditSerializer(user,data=request.data,)


class UserList(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
