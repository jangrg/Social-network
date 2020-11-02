from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action

from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from rest_framework.response import Response


class OnlyFieldsSerializerMixin:
    def get_serializer(self, *args, **kwargs):
        kwargs['only_fields'] = self.only_fields
        return super().get_serializer(*args, **kwargs)


class AccountViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['only_fields'] = ['password', 'username', 'first_name', 'last_name', 'email', 'birth_date']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'confirm' or self.action == 'logout':
            return None
        elif self.action == 'login':
            kwargs['only_fields'] = ['password', 'username']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'follow':
            kwargs['only_fields'] = ['id']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'retrieve':
            kwargs['only_fields'] = ['id', 'username', 'first_name', 'last_name', 'email', 'birth_date']
            return super().get_serializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            send_mail(
                'Account confirmation WeShare',
                f'Confirm your account on this link: localhost:3000/account/confirm/{user.id}/',
                'noreply@somehost.local',
                [user.email],
            )
            return Response(
                {'message': 'Check your email to confirm account!'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], name='confirm')
    def confirm(self, request, pk=None):
        user = self.get_object()
        if user is not None and not user.is_active:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'], name='login')
    def login(self, request, *args, **kwargs):
        user = auth.authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is not None and user.is_active:
            auth.login(request, user)
            return Response(
                {'user': UserSerializer(user, only_fields=['id', 'username', 'first_name', 'last_name', 'email',
                                                           'birth_date']).data},
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['GET'], name='logout')
    def logout(self, request, *args, **kwargs):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], name='add_following')
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        user = request.user
        if user.id != user_to_follow.id:
            user.following.add(user_to_follow)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['GET'], name='followed_posts')
    def followed_posts(self, request):
        user = request.user
        posts = user.following.posts
        serializer = PostSerializer(posts)
        return Response(serializer.data, status=status.HTTP_200_OK)
