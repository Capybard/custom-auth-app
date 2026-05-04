from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Session
from .services import hash_token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get("Authorization")

        if not header:
            return None

        if not header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid authorization header")

        raw_token = header.replace("Bearer ", "")
        token_hash = hash_token(raw_token)

        session = (
            Session.objects
            .select_related("user")
            .filter(
                token_hash=token_hash,
                revoked_at__isnull=True,
                expires_at__gt=timezone.now(),
                user__is_active=True,
            )
            .first()
        )

        if not session:
            raise AuthenticationFailed("Invalid or expired token")

        return session.user, session