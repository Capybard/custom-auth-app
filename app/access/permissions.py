from rest_framework.permissions import BasePermission
from .services import user_has_permission


class HasRBACPermission(BasePermission):
    resource = None
    action = None

    def has_permission(self, request, view):
        if not request.user:
            return False

        resource = getattr(view, "resource", None)
        action = getattr(view, "action_name", None)

        if not resource or not action:
            return False

        return user_has_permission(request.user, resource, action)