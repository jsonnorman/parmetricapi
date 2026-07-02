from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from parmetricapi.views import Courses, TeeBoxes, Holes, Favorites, login_user, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"courses", Courses, "course")
router.register(r"tee_boxes", TeeBoxes, "tee_box")
router.register(r"holes", Holes, "hole")
router.register(r"favorites", Favorites, "favorite")


urlpatterns = [
    path("", include(router.urls)),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("register", register_user),
    path("login", login_user),
]
