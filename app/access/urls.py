from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    AdminRoleListCreateView,
    AdminResourceListCreateView,
    AdminPermissionListCreateView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),

    path("profile/", ProfileView.as_view()),

    path("admin/roles/", AdminRoleListCreateView.as_view()),
    path("admin/resources/", AdminResourceListCreateView.as_view()),
    path("admin/permissions/", AdminPermissionListCreateView.as_view()),
]