from django.contrib import auth
from django.http import HttpResponseRedirect
import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action

from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class OnlyFieldsSerializerMixin:
    def get_serializer(self, *args, **kwargs):
        kwargs['only_fields'] = self.only_fields
        return super().get_serializer(*args, **kwargs)


class AccountViewSet(OnlyFieldsSerializerMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    only_fields = ['password', 'username', 'first_name', 'last_name', 'email', 'birth_date']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user = auth.authenticate(username=user.username, password=request.data.get('password'))
            auth.login(request, user)
            return Response(
                {'user': UserSerializer(user, only_fields=['username', 'first_name', 'last_name', 'email', 'birth_date']).data},
                status=status.HTTP_201_CREATED
            )
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionViewSet(OnlyFieldsSerializerMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    only_fields = ['username', 'password']

    @action(detail=False, methods=['POST'], name='login')
    def login(self, request, *args, **kwargs):
        # serializer = self.serializer_class(data=request.data)
        if True:  # serializer.is_valid():
            user = auth.authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None and user.is_active:
                auth.login(request, user)
                return Response({'user': UserSerializer(user, only_fields=['username', 'first_name', 'last_name', 'email', 'birth_date']).data})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], name='logout')
    def logout(self, request, *args, **kwargs):
        print(request.user)
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)


class TimeView(APIView):

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({
            'now': now,
            'user': UserSerializer(request.user, only_fields=['username', 'email']).data
        })
