from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import UserRegistrationSerializer, PostCreateSerializer, LikeSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Post, Like
from rest_framework.exceptions import ValidationError


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерируем JWT токены
        refresh = RefreshToken.for_user(user)

        # Формируем ответ с данными пользователя и токенами
        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'token': str(refresh.access_token),
            'refresh': str(refresh),
        })


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]


class PostView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet,  mixins.UpdateModelMixin,
               mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Проверка, является ли текущий пользователь автором статьи
        post = self.get_object()
        if post.author != self.request.user:
            raise ValidationError({"detail": "У вас нет прав для изменения этой статьи."})
        serializer.save()

    def perform_destroy(self, instance):
        # Проверка, является ли текущий пользователь автором статьи
        if instance.author != self.request.user:
            raise ValidationError({"detail": "У вас нет прав для удаления этой статьи."})
        instance.delete()

class LikePostView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)


class UnlikePostView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        post_id = self.kwargs['post_id']
        return Like.objects.get(post_id=post_id, user=user)