from common.models import User, Post
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
    following = SerializerMethodField('get_following')
    followers = SerializerMethodField('get_followers')

    class Meta:
        model = User
        fields = '__all__'

    def get_following(self, user):
        return UserSerializer(user.following.all(), many=True, only_fields=['id','username', 'password']).data

    def get_followers(self, user):
        return UserSerializer(user.followers.all(), many=True, only_fields=['id','username', 'password']).data

    def create(self):
        obj = User.objects.create_user(**self.validated_data)
        return obj

    def save(self):
        obj = User.objects.create_user(**self.validated_data)
        return obj

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'posted_by', 'content', 'photo', 'type_attr', 'likes_num', 'time']
