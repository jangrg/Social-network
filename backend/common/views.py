from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status, filters, generics
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
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
            kwargs['only_fields'] = ['password', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'is_private']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'confirm':
            return None
        elif self.action == 'comment':
            kwargs['only_fields'] = ['text', 'likes_num', 'post']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'follow':
            kwargs['only_fields'] = ['id']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'retrieve' or self.action == 'logged_user_data':
            kwargs['only_fields'] = ['id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'is_private']
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
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PostViewSet(viewsets.ModelViewSet):

    serializer_class = Post
    parser_class = (FileUploadParser,)

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        if self.request:
            context.update({'user': self.request.user})
        return context

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'comment':
            return CommentSerializer
        else:
            return PostSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['only_fields'] = ['content', 'image']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'list':
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'comment':
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'like' or self.action == 'unlike':
            kwargs['only_fields'] = ['id']
            return super().get_serializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'read': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'delete': [IsAuthenticated],
        'followed_posts': [IsAuthenticated],
        'comment': [IsAuthenticated],
        }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            post = serializer.save(posted_by=request.user)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_id = self.request.query_params.get('by_user', None)
        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = queryset.filter(posted_by=user)
        return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], name='followed_posts')
    def followed_posts(self, request):
        return Response(
            self.get_serializer(Post.objects.filter(posted_by__in=request.user.following.all()), many=True).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'], name='comment')
    def comment(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            data['posted_by'] = request.user
            data['post'] = Post.objects.filter(id=data['post']).first()
            comment = Comment.objects.create(**data)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], name='comment')
    def get_comment(self, request):
        return Response(CommentSerializer(Comment.objects.all(), many=True).data)

    @action(detail=True, methods=['POST'], name='like')
    def like(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            post = self.get_object()
            if post is not None:
                user = post.liked_by.filter(id=request.user.id)
                if not user:
                    post.likes_num += 1
                    post.liked_by.add(request.user)
                post.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['POST'], name='like')
    def unlike(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            post = self.get_object()
            if post is not None:
                user = post.liked_by.filter(id=request.user.id)
                if user:
                    post.likes_num -= 1
                    post.liked_by.remove(request.user)
                post.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
