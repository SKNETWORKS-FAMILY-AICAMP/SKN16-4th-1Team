from fastapi import APIRouter, HTTPException
import jwt

from .common import (
    store,
    pwd_ctx,
    issue_token,
    ensure_user_indexes,
    get_user_by_email,
    next_id,
    now,
    JWT_ALG,
    JWT_SECRET,
    SignupRequest,
    LoginRequest,
    TokenRefreshRequest,
    UserOut,
    AuthResponse,
    EmailRequest,
    EmailToken,
    PasswordResetRequest,
    PasswordResetConfirm,
)


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut)
def signup(payload: SignupRequest):
    if get_user_by_email(str(payload.email)):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = next_id("user")
    user = {
        "id": user_id,
        "username": payload.username,
        "email": str(payload.email),
        "password_hash": pwd_ctx.hash(payload.password),
        "created_at": now(),
        "last_login": None,
        "email_verified": False,
    }
    ensure_user_indexes(user)
    
    return UserOut(id=user_id, username=user["username"], email=user["email"])


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    user = get_user_by_email(str(payload.email))
    if not user or not pwd_ctx.verify(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user["last_login"] = now()
    access = issue_token(user["id"], "access")
    refresh = issue_token(user["id"], "refresh")
    return AuthResponse(
        access=access,
        refresh=refresh,
        user=UserOut(id=user["id"], username=user["username"], email=user["email"]),
    )


@router.post("/refresh")
def refresh_token(payload: TokenRefreshRequest):
    try:
        decoded = jwt.decode(payload.refresh, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user_id = decoded.get("sub")
    if user_id not in store["users"]:
        raise HTTPException(status_code=401, detail="User not found")
    return {"access": issue_token(user_id, "access")}


@router.post("/verify-email/request")
def verify_email_request(payload: EmailRequest):
    # Stub: pretend an email was sent
    return {"ok": True}


@router.post("/verify-email/confirm")
def verify_email_confirm(payload: EmailToken):
    # Stub: mark first user as verified if exists
    if store["users"]:
        any_user = next(iter(store["users"].values()))
        any_user["email_verified"] = True
    return {"ok": True}


@router.post("/password/forgot")
def password_forgot(payload: PasswordResetRequest):
    # Stub: issue reset token via email
    return {"ok": True}


@router.post("/password/reset")
def password_reset(payload: PasswordResetConfirm):
    # Stub: accept token and set password for the first user
    if store["users"]:
        any_user = next(iter(store["users"].values()))
        any_user["password_hash"] = pwd_ctx.hash(payload.new_password)
    return {"ok": True}
