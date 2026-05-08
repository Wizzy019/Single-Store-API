from fastapi import APIRouter, Depends
from models.user import User
from auth.dependencies import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/Protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "messagee": "Access granted",
        "user": {
            "id" : current_user.id,
            "email": current_user.email,
            "name": current_user.name
        }
    }