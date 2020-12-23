from django.contrib import auth
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import viewsets, mixins, status, filters, generics
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated

from .models import User, Post, Comment, Message, Page
from .serializers import UserSerializer, PostSerializer, CommentSerializer, MessageSerializer, PageSerializer
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
        elif self.action == 'comment':
            kwargs['only_fields'] = ['text', 'likes_num', 'post']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'follow':
            kwargs['only_fields'] = ['id']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'retrieve' or self.action == 'logged_user_data':
            kwargs['only_fields'] = ['id', 'username', 'first_name', 'last_name', 'email', 'birth_date']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'send_message':
            kwargs['only_fields'] = ['id', 'sender', 'receiver', 'text_content', 'photo']
            return MessageSerializer(*args, **kwargs)
        elif self.action == 'get_messages':
            kwargs['only_fields'] = []
            return MessageSerializer(*args, **kwargs)
        elif self.action == 'get_messaged_users':
            kwargs['only_fields'] = ['id', 'username', 'first_name', 'last_name']
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

    @action(detail=True, methods=['POST'], name='send_message')
    def send_message(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                print(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['POST'], name='send_message')
    def get_messages(self, request, pk=None):
        user = request.user
        other_user = self.get_object()
        if user.is_authenticated:
            messages = Message.objects.filter((Q(sender=user) & Q(receiver=other_user)) |
                                              (Q(sender=other_user) & Q(receiver=user)))
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['GET'], name='send_message')
    def get_messaged_users(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            users = User.objects.filter(Q(sent_messages__receiver=user) | Q(received_messages__sender=user)).distinct()
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PostViewSet(viewsets.ModelViewSet):
    parser_class = (FileUploadParser,)

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        if self.request:
            context.update({'user': self.request.user})
        return context

    def get_queryset(self):
        if self.action == 'comment' or self.action == 'like_comment' or self.action == 'unlike_comment':
            return Comment.objects.all()
        return Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'comment' or self.action == 'like_comment' or self.action == 'unlike_comment':
            return CommentSerializer
        else:
            return PostSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['only_fields'] = ['content', 'image', 'is_private', 'is_page']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'partial_update':
            kwargs['only_fields'] = ['content', 'image', 'is_private', 'is_page']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'list':
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'comment':
            kwargs['only_fields'] = ['comment_text', 'post']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'like' or self.action == 'unlike':
            kwargs['only_fields'] = ['id']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'like_comment' or self.action == 'unlike_comment':
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
        'like_comment': [IsAuthenticated],
        'unlike_comment': [IsAuthenticated],
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
            return Response(data=PostSerializer(post, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        current_user = request.user

        user_id = self.request.query_params.get('by_user', None)
        page_id = self.request.query_params.get('on_page', None)

        if page_id:
            page = Page.objects.get(id=page_id)
            queryset = queryset.filter(is_page=True, page=page)

        if user_id:
            user = User.objects.get(id=user_id)
            print(user)
            queryset = queryset.filter(posted_by=user)
            if current_user.username != user.username:
                if not current_user.following.filter(id=user_id).exists():
                    queryset = queryset.filter(is_private=False)
        else:
            queryset = queryset.filter(is_private=False)
        return Response(self.get_serializer(queryset, many=True).data, status=status.HTTP_200_OK)
    #
    # def get_posts_from_pages

    @action(detail=False, methods=['GET'], name='followed_posts')
    def followed_posts(self, request):
        return Response(
            self.get_serializer(
                Post.objects.filter(posted_by__in=request.user.following.all()) | Post.objects.filter(
                    posted_by=request.user.id),
                many=True
            ).data,
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

    @action(detail=True, methods=['POST'], name='like_comment')
    def like_comment(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if user in comment.liked_by.all():
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        comment.likes_num += 1
        comment.liked_by.add(user)
        comment.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], name='unlike_comment')
    def unlike_comment(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        if user in comment.liked_by.all():
            comment.likes_num -= 1
            comment.liked_by.remove(user)
            comment.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_208_ALREADY_REPORTED)

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

    @action(detail=True, methods=['POST'], name='unlike')
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


class CommentViewSet(mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class PageViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return PageSerializer

    def get_queryset(self):
        return Page.objects.all()

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'read': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'delete': [IsAuthenticated],
        'my_page': [IsAuthenticated]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(owner=request.user)
        except IntegrityError as error:
            return Response("Page for this user already exists!", status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'], name="my_page")
    def my_page(self, request, *args, **kwargs):
        current_user = request.user
        try:
            page = Page.objects.get(owner=current_user)
            return Response(PageSerializer(page).data, status=status.HTTP_200_OK)
        except:
            return Response({"No page available."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'], name="my_page")
    def get_posts_from_page(self, request, *args, **kwargs):
        page = self.get_object()
        owner_id = page.owner_id
        posts = Post.objects.filter(Q(posted_by__id=owner_id) & Q(is_page=True))
        return Response(PostSerializer(posts, context={'request': request}, many=True).data)


class Search(viewsets.ViewSet):
    filter_backends = [filters.SearchFilter]
    filter_backends[0].search_param = "query"
    filter_backends[0].search_title = "Query"

    def list(self, request, **kwargs):
        query = self.request.query_params.get('query', None)
        users = User.objects.all()
        pages = Page.objects.all()

        if query:
            users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
            pages = Page.objects.filter(name__icontains=query)

        return JsonResponse({
            "users": UserSerializer(users, many=True).data,
            "pages": PageSerializer(pages, many=True).data
        })
