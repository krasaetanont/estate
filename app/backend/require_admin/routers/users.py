from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.database import get_db
from app.dependencies.auth import hash_password
from app.dependencies.guards import get_current_user, require_admin
from app.models.models import User, UserRoleEnum
from app.schemas.schemas import PaginatedUsers, UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])


# ─── Admin: List All Users ────────────────────────────────────────────────────

@router.get("", response_model=PaginatedUsers)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: UserRoleEnum = None,
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all users. Admin only."""
    query = select(User)
    if role:
        query = query.where(User.user_role == role)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size).order_by(User.created_at.desc()))
    users = result.scalars().all()

    return PaginatedUsers(
        total=total,
        page=page,
        page_size=page_size,
        results=[UserOut.model_validate(u) for u in users],
    )


# ─── Admin: Get Single User ───────────────────────────────────────────────────

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get a single user by ID. Admin only."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)


# ─── Admin: Create User ───────────────────────────────────────────────────────

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate,
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new user account. Admin only.
    For public self-registration, use POST /api/auth/register instead.
    """
    # Check email uniqueness
    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
        user_role=body.user_role,
        phone_number=body.phone_number,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut.model_validate(user)


# ─── Admin: Update User ───────────────────────────────────────────────────────

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    body: UserUpdate,
    _: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update user details (role, verification, etc.). Admin only."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut.model_validate(user)


# ─── Admin: Delete User ───────────────────────────────────────────────────────

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a user account. Admin only. Cannot delete yourself."""
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()


# ─── Self: Get My Profile ─────────────────────────────────────────────────────

@router.get("/me/profile", response_model=UserOut)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user's profile."""
    return UserOut.model_validate(current_user)