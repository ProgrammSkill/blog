from .views import UserRegistrationView, PostView,CreatePostView, LikePostView, UnlikePostView, CreatePostView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


router = DefaultRouter()
router.register('post', PostView, 'post'),

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('post-create', CreatePostView.as_view(), name='post-create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]


