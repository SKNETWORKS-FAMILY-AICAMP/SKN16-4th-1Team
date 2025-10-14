from fastapi import APIRouter, Depends

from .common import get_current_user


router = APIRouter(prefix="/api", tags=["bootstrap"])


@router.get("/bootstrap")
def bootstrap(user=Depends(get_current_user)):
    return {
        "me": {"id": user["id"], "username": user["username"], "email": user["email"]},
        "notifications": {"unread": 0},
        "flags": {"beta": True},
        "banner": {"title": "Welcome", "link": None},
        "links": [
            {"rel": "profile", "href": "/api/profile/me"},
            {"rel": "diaries", "href": "/api/diaries"},
        ],
    }
