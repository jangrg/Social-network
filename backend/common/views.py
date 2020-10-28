from django.contrib import auth
from django.core.mail import send_mail
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
            user.is_active = False
            user.save()
            send_mail(
                # title:
                "Password Reset for {title}".format(title="Some website title"),
                # message:
                f'Confirm your account on this link: localhost:3000/account/confirm/{user.id}/',
                # from:
                "noreply@somehost.local",
                # to:
                [user.email]
            )
            return Response(
                {'message': 'Check your email to confirm account!'},
                status=status.HTTP_200_OK
            )
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionViewSet(OnlyFieldsSerializerMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    only_fields = ['username', 'password']

    @action(detail=False, methods=['POST'], name='login')
    def login(self, request, *args, **kwargs):
        user = auth.authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is not None and user.is_active:
            auth.login(request, user)
            return Response(
                {'user': UserSerializer(user, only_fields=['username', 'first_name', 'last_name', 'email',
                                                           'birth_date']).data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['GET'], name='logout')
    def logout(self, request, *args, **kwargs):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], name='confirm')
    def confirm(self, request, pk=None):
        if pk is not None:
            user = User.objects.filter(id=pk).first()
            if user is not None and not user.is_active:
                user.is_active = True
                user.save()
                user = auth.authenticate(username=user.username, password=request.data.get('password'))
                auth.login(request, user)
                return Response(
                    {'user': UserSerializer(user, only_fields=['username', 'first_name', 'last_name', 'email',
                                                               'birth_date']).data}
                    , status=status.HTTP_201_CREATED
                )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# example api view, used to check whether user is logged in
class TimeView(APIView):

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        return Response({
            'now': now,
            'user': UserSerializer(request.user, only_fields=['username', 'email']).data
        })
