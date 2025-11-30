from rest_framework.authentication import BaseAuthentication
from .auth_utils import verify_token
from .models import ScannerUser


class ScannerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return None

        token = auth.split("Bearer ")[1]
        user_id = verify_token(token)

        if not user_id:
            return None

        user = ScannerUser.objects.filter(id=user_id).first()

        if not user:
            return None

        return (user, None)
