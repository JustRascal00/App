from ninja import Router
from django.contrib.auth import get_user_model
from django.conf import settings
from jose import jwt
from datetime import datetime, timezone
from typing import Dict

router = Router()
User = get_user_model()

@router.post("/token")
def login(request, username: str, password: str) -> Dict:
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        payload = {
            "user_id": user.id,
            "exp": datetime.now(timezone.utc) + settings.JWT_ACCESS_TOKEN_LIFETIME
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return {"access": token}
    return {"error": "Invalid credentials"}

@router.post("/register")
def register(request, username: str, email: str, password: str) -> Dict:
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return {"message": "Registration successful"}
    except Exception as e:
        return {"error": str(e)}