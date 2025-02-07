from django.urls import path
from v1 import api


urlpatterns = [
    path('', api.api.urls),
]
