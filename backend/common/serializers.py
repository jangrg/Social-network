from common.models import User, Post, Comment, Message, Page
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `only_fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('only_fields', None)
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self):
        obj = User.objects.create_user(**self.validated_data)
        return obj

    def save(self):
        obj = User.objects.create_user(**self.validated_data)
        return obj


class CommentSerializer(DynamicFieldsModelSerializer):
    posted_by = UserSerializer(only_fields=['id', 'username'], read_only=True)
    liked_by = UserSerializer(only_fields=['id', 'username'], many=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'likes_num', 'post', 'posted_by', 'liked_by']


class PostSerializer(DynamicFieldsModelSerializer):
    posted_by = UserSerializer(only_fields=['id', 'username'], read_only=True)
    liked_by = UserSerializer(only_fields=['id', 'username'], many=True)
    comments = SerializerMethodField()
    logged_user_liked = SerializerMethodField()
    # image = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'posted_by', 'content', 'image', 'type_attr', 'likes_num', 'time', 'comments', 'liked_by', 'logged_user_liked']

    def get_comments(self, obj):
        return CommentSerializer(
            Comment.objects.filter(post=obj.id).all(),
            many=True,
            # only_fields=['id', 'comment_text', 'likes_num', 'posted_by', 'liked_by']
        ).data

    def get_logged_user_liked(self, obj):
        if self.context.get('user'):
            if self.context.get('user') in obj.liked_by.all():
                return True
        return False


class MessageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    # def get_image(self, obj):
    #     request = self.context.get('request')
    #     photo_url = obj.photo.url
    #     return request.build_absolute_uri(photo_url)


class PageSerializer(DynamicFieldsModelSerializer):

    owner = UserSerializer(only_fields=['id', 'username'], read_only=True)

    class Meta:
        model = Page
        fields = ['owner', 'name', 'work_time', 'date_created', 'location', 'categories']
