from rest_framework.authentication import BaseAuthentication
from .auth_utils import verify_token
from .models import AuthUsers

class ScannerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")

        if not auth:
            return None

        if auth.startswith("Bearer "):
            token = auth.split("Bearer ")[1]

        elif auth.startswith("Token "):
            token = auth.split("Token ")[1]

        else:
            token = auth.strip()

        user_id = verify_token(token)
        if not user_id:
            return None

        user = AuthUsers.objects.filter(id=user_id).first()
        if not user:
            return None

        return (user, None)

