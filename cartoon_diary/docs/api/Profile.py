from fastapi import APIRouter, Depends

from .common import (
    store,
    get_current_user,
    ProfileUpdate,
    ProfileOut,
)


router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("/me", response_model=ProfileOut)
def get_profile(user=Depends(get_current_user)):
    profile = store["profiles"].get(user["id"]) or {}
    profile.update({"email": user["email"], "username": user["username"]})
    return profile


@router.put("/me", response_model=ProfileOut)
def update_profile(payload: ProfileUpdate, user=Depends(get_current_user)):
    profile = store["profiles"].setdefault(user["id"], {})
    for k, v in payload.model_dump(exclude_none=True).items():
        profile[k] = v
    profile.update({"email": user["email"], "username": user["username"]})
    return profile
