import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    following = models.ManyToManyField('User', blank=True, related_name='followers', symmetrical=False)


class Category(models.Model):
    name = models.CharField(max_length=100)
    pages = models.ForeignKey


class Page(models.Model):
    # Not sure what field type this should be
    work_time = models.CharField(null=True, max_length=100)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name="pages")
    owner = models.ForeignKey(User, related_name="pages", on_delete=models.CASCADE)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    posted_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    photo = models.CharField(null=True, blank=True, max_length=255)
    type_attr = models.CharField(null=True, blank=True, max_length=255)
    likes_num = models.IntegerField(null=True, blank=True, default=0)
    time = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(Page, related_name="posts", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time']


class Item(models.Model):
    size = models.IntegerField()
    photo = models.URLField()
    price = models.FloatField()
    rating = models.FloatField(null=True)
    text_content = models.TextField()
    quantity_left = models.IntegerField()
    category = models.ForeignKey(Category, related_name="items_in_category", on_delete=models.CASCADE)
    user_seller = models.ForeignKey(User, related_name="items_for_sale", null=True, on_delete=models.CASCADE)
    page_seller = models.ForeignKey(Page, related_name="items_for_sale", null=True, on_delete=models.CASCADE)


class Review(models.Model):
    likes_num = models.IntegerField(default=0)
    rating = models.FloatField(null=True)
    text = models.TextField()
    sellers_answer = models.TextField(null=True)
    item = models.ForeignKey(Item, related_name="review", on_delete=models.CASCADE)


class Message(models.Model):
    time_sent = models.DateTimeField(default=timezone.now)
    photo = models.URLField(null=True)
    text_content = models.TextField()
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)


class Notification(models.Model):
    time_created = models.DateTimeField(default=timezone.now)
    text_content = models.TextField()
    marked_as_read = models.BooleanField(default=False)
    # Not sure what field type this should be
    color = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    likes_num = models.IntegerField(null=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    # parent_comment = models.ForeignKey("Comment", related_name="comment", on_delete=models.CASCADE)
