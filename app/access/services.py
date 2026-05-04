import hashlib
import secrets
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from .models import Session, Permission


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_session(user):
    raw_token = secrets.token_urlsafe(32)

    Session.objects.create(
        user=user,
        token_hash=hash_token(raw_token),
        expires_at=timezone.now() + timedelta(days=7),
    )

    return raw_token


def verify_password(raw_password, password_hash):
    return check_password(raw_password, password_hash)


def make_password_hash(raw_password):
    return make_password(raw_password)


def user_has_permission(user, resource_code, action_code):
    return Permission.objects.filter(
        role__userrole__user=user,
        resource__code=resource_code,
        action__code=action_code,
    ).exists()