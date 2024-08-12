from django.urls import include, path
from blog_app.views import PostList
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('list-posts/', PostList, name='post-list'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path("api/", include("blog_app.api.urls")),
]