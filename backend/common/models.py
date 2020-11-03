import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = 'localhost:3000/resetpassword&token={}'.format(reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    following = models.ManyToManyField('User', blank=True, related_name='followers', symmetrical=False)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    posted_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    photo = models.CharField(null=True, blank=True, max_length=255)
    type_attr = models.CharField(null=True, blank=True, max_length=255)
    likes_num = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    