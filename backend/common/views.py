from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status, filters, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from rest_framework.response import Response


class OnlyFieldsSerializerMixin:
    def get_serializer(self, *args, **kwargs):
        kwargs['only_fields'] = self.only_fields
        return super().get_serializer(*args, **kwargs)


class AccountViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_serializer_class(self):
        return UserSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['only_fields'] = ['password', 'username', 'first_name', 'last_name', 'email', 'birth_date']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'confirm':
            return None
        elif self.action == 'follow':
            kwargs['only_fields'] = ['id']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'retrieve' or self.action == 'logged_user_data':
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

    @action(detail=True, methods=['POST'], name='add_following')
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        user = request.user
        if user.id != user_to_follow.id:
            user.following.add(user_to_follow)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], name='logged_user_data')
    def logged_user_data(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return Response(
                {'user': self.get_serializer(user).data},
                status = status.HTTP_200_OK
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'read': [IsAuthenticated],
                                    'update': [IsAuthenticated],
                                    'partial_update': [IsAuthenticated],
                                    'delete': [IsAuthenticated],
                                    'followed_posts': [IsAuthenticated]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['GET'], name='followed_posts')
    def followed_posts(self, request):
        # needs to be fixed after database is populated
        print(request.user.following)
        return Response(self.get_serializer(request.user.following.posts, many=True).data, status=status.HTTP_200_OK)
