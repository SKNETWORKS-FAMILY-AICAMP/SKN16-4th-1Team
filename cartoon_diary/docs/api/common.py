from datetime import datetime, timedelta , timezone
from typing import Optional, List, Dict, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field


# In-memory store (simple stub)
store: Dict[str, Any] = {
    "users": {},  # user_id -> dict
    "users_by_email": {},
    "profiles": {},  # user_id -> dict
    "diaries": {},  # diary_id -> dict
    "diaries_by_user": {},  # user_id -> list of diary_ids
    "cartoons": {},  # diary_id -> dict
    "tasks": {},  # task_id -> dict
    "seq": {"user": 1, "diary": 1, "task": 1},
}


JWT_SECRET = "dev-secret-change-me"
JWT_ALG = "HS256"
ACCESS_MIN = 30
REFRESH_DAYS = 7

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)


KST = timezone(timedelta(hours=9))  # UTC+9 (한국 표준시)

def now() -> datetime:
    return datetime.now(KST)


def issue_token(user_id: str, token_type: str) -> str:
    exp = now() + (timedelta(minutes=ACCESS_MIN) if token_type == "access" else timedelta(days=REFRESH_DAYS))
    payload = {"sub": user_id, "type": token_type, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def get_current_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer)) -> dict:
    """Auth 제거 버전: 토큰 없이도 기본 사용자(anonymous)를 반환.

    기존 JWT 검증 대신, 최초 호출 시 기본 사용자(guest)를 생성해 사용합니다.
    """
    # Ensure an anonymous default user exists
    anon_id = "anon"
    user = store["users"].get(anon_id)
    if not user:
        user = {
            "id": anon_id,
            "username": "guest",
            "email": "guest@example.com",
            "password_hash": pwd_ctx.hash("guest"),
            "created_at": now(),
            "last_login": now(),
            "email_verified": True,
        }
        store["users"][anon_id] = user
        store["users_by_email"][user["email"].lower()] = user
        store["profiles"][anon_id] = {
            "display_name": "Guest",
            "avatar_url": None,
            "preferences": {},
            "email": user["email"],
            "username": user["username"],
        }
    return user


def next_id(kind: str) -> str:
    store["seq"][kind] += 1
    return str(store["seq"][kind] - 1)


def ensure_user_indexes(user: dict):
    store["users"][user["id"]] = user
    store["users_by_email"][user["email"].lower()] = user
    if user["id"] not in store["profiles"]:
        store["profiles"][user["id"]] = {
            "display_name": user["username"],
            "avatar_url": None,
            "preferences": {},
            "email": user["email"],
            "username": user["username"],
        }


def get_user_by_email(email: str) -> Optional[dict]:
    return store["users_by_email"].get(email.lower())


def new_task(task_type: str, diary_id: Optional[str] = None) -> dict:
    task_id = next_id("task")
    task = {
        "id": task_id,
        "diary_id": diary_id,
        "type": task_type,
        "status": "queued",
        "progress": 0,
        "worker_logs": ["queued"],
        "error_message": None,
        "created_at": now(),
        "finished_at": None,
    }
    store["tasks"][task_id] = task
    return task


def maybe_complete_task(task: dict):
    if task["status"] in ("succeeded", "failed"):
        return
    elapsed = (now() - task["created_at"]).total_seconds()
    if elapsed > 1.5:
        task["status"] = "succeeded"
        task["progress"] = 100
        task["worker_logs"].append("done")
        task["finished_at"] = now()
        if task.get("diary_id"):
            diary_id = task["diary_id"]
            store["cartoons"][diary_id] = {
                "status": "succeeded",
                "panels": [
                    {"index": i + 1, "image_url": f"https://example.com/img/{diary_id}-{i+1}.png", "caption": None}
                    for i in range(4)
                ],
                "meta": {"seed": 1234, "style": 1},
            }


# Schemas (shared)
class SignupRequest(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRefreshRequest(BaseModel):
    refresh: str


class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr


class AuthResponse(BaseModel):
    access: str
    refresh: str
    user: UserOut


class EmailRequest(BaseModel):
    email: EmailStr


class EmailToken(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=6)


class ProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class ProfileOut(ProfileUpdate):
    email: EmailStr
    username: str


class DiaryCreate(BaseModel):
    date: str  # YYYY-MM-DD
    title: str
    content: str


class DiaryOut(BaseModel):
    id: str
    date: str
    title: str
    content: str
    created_at: datetime


class DiaryListOut(BaseModel):
    items: List[DiaryOut]
    next_cursor: Optional[str] = None


class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class GenerateRequest(BaseModel):
    style: Optional[int] = Field(default=1)
    panels: Optional[int] = Field(default=4)
    language: Optional[str] = Field(default="ko")


class CartoonPanelOut(BaseModel):
    index: int
    image_url: str
    caption: Optional[str] = None


class CartoonOut(BaseModel):
    status: str
    panels: List[CartoonPanelOut] = []
    meta: Dict[str, Any] = {}


class RerollRequest(BaseModel):
    style: Optional[int] = None
    variation_seed: Optional[int] = None
    keep_layout: Optional[bool] = None


class TaskOut(BaseModel):
    id: str
    diary_id: Optional[str] = None
    type: str
    status: str
    progress: int
    worker_logs: Optional[List[str]] = None
    error_message: Optional[str] = None
    created_at: datetime
    finished_at: Optional[datetime] = None
