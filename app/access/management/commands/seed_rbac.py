from django.core.management.base import BaseCommand
from access.models import User, Role, UserRole, Resource, Action, Permission
from access.services import make_password_hash


class Command(BaseCommand):
    help = "Creates test users, roles, resources, actions and permissions"

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "first_name": "Admin",
                "last_name": "Admin",
                "password_hash": make_password_hash("admin123"),
            },
        )

        user, _ = User.objects.get_or_create(
            email="user@example.com",
            defaults={
                "first_name": "User",
                "last_name": "User",
                "password_hash": make_password_hash("user123"),
            },
        )

        admin_role, _ = Role.objects.get_or_create(
            code="admin",
            defaults={"name": "Administrator"},
        )

        user_role, _ = Role.objects.get_or_create(
            code="user",
            defaults={"name": "User"},
        )

        UserRole.objects.get_or_create(user=admin, role=admin_role)
        UserRole.objects.get_or_create(user=user, role=user_role)

        resource_codes = ["profile", "permissions", "reports", "orders"]
        action_codes = ["create", "read", "update", "delete"]

        for code in resource_codes:
            Resource.objects.get_or_create(
                code=code,
                defaults={"name": code},
            )

        for code in action_codes:
            Action.objects.get_or_create(
                code=code,
                defaults={"name": code},
            )

        for resource in Resource.objects.all():
            for action in Action.objects.all():
                Permission.objects.get_or_create(
                    role=admin_role,
                    resource=resource,
                    action=action,
                )

        Permission.objects.get_or_create(
            role=user_role,
            resource=Resource.objects.get(code="orders"),
            action=Action.objects.get(code="read"),
        )

        Permission.objects.get_or_create(
            role=user_role,
            resource=Resource.objects.get(code="profile"),
            action=Action.objects.get(code="read"),
        )

        Permission.objects.get_or_create(
            role=user_role,
            resource=Resource.objects.get(code="profile"),
            action=Action.objects.get(code="update"),
        )

        self.stdout.write(
            self.style.SUCCESS("RBAC test data created successfully")
        )