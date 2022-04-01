from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from users.api.api import UserViewSet

router = DefaultRouter()

router.register('',UserViewSet, basename= "users")

urlpatterns = router.urls