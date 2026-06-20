from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from parmetricapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"courses", Courses, "course")


urlpatterns = [
    path("", include(router.urls)),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("register", register_user),
    path("login", login_user),
]
