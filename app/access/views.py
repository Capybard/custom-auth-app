from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Session, Role, Resource, Action, Permission
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    RoleSerializer,
    ResourceSerializer,
    ActionSerializer,
    PermissionSerializer,
)
from .services import (
    create_session,
    make_password_hash,
    verify_password,
)
from .permissions import HasRBACPermission


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if data["password"] != data["repeat_password"]:
            return Response({"detail": "Passwords do not match"}, status=400)

        if User.objects.filter(email=data["email"]).exists():
            return Response({"detail": "Email already exists"}, status=400)

        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data.get("middle_name", ""),
            email=data["email"],
            password_hash=make_password_hash(data["password"]),
        )

        return Response(ProfileSerializer(user).data, status=201)


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            email=serializer.validated_data["email"],
            is_active=True,
        ).first()

        if not user:
            return Response({"detail": "Invalid credentials"}, status=401)

        if not verify_password(
            serializer.validated_data["password"],
            user.password_hash,
        ):
            return Response({"detail": "Invalid credentials"}, status=401)

        token = create_session(user)

        return Response({"token": token})


class LogoutView(APIView):
    def post(self, request):
        session = request.auth
        session.revoked_at = timezone.now()
        session.save(update_fields=["revoked_at"])

        return Response({"detail": "Logged out"})


class ProfileView(APIView):
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    def patch(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.deleted_at = timezone.now()
        user.save(update_fields=["is_active", "deleted_at"])

        Session.objects.filter(user=user, revoked_at__isnull=True).update(
            revoked_at=timezone.now()
        )

        return Response({"detail": "Account deleted"})
    
class AdminRoleListCreateView(APIView):
    permission_classes = [HasRBACPermission]
    resource = "permissions"
    action_name = "update"

    def get(self, request):
        return Response(RoleSerializer(Role.objects.all(), many=True).data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class AdminResourceListCreateView(APIView):
    permission_classes = [HasRBACPermission]
    resource = "permissions"
    action_name = "update"

    def get(self, request):
        return Response(ResourceSerializer(Resource.objects.all(), many=True).data)

    def post(self, request):
        serializer = ResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class AdminPermissionListCreateView(APIView):
    permission_classes = [HasRBACPermission]
    resource = "permissions"
    action_name = "update"

    def get(self, request):
        return Response(PermissionSerializer(Permission.objects.all(), many=True).data)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)