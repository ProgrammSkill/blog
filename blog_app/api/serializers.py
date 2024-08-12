from django.contrib.auth.models import User
from rest_framework import serializers
from blog_app.models import Post, Like
from rest_framework.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('title', 'content', 'author')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('post', 'user')

    def validate(self, attrs):
        user = self.context['request'].user
        post = attrs.get('post')

        # Проверяем, существует ли уже лайк от этого пользователя на этот пост
        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError("Вы уже поставили лайк на этот пост.")

        return attrs