from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.deps_auth import get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.crud.user import get_by_email, create_user
from app.schemas.auth import RegisterIn, TokenOut
from app.schemas.user import UserOut
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    
    if len(data.password) < 10:
        raise HTTPException(status_code=400, detail="Password must be at least 10 characters")
    pw_bytes = data.password.encode("utf-8")
    if len(pw_bytes) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 bytes for bcrypt)")
    existing = get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    user = create_user(db, email=data.email, password_hash=hash_password(data.password), role="user")
    
    return user

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm usa: username + password
    user = get_by_email(db, form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user