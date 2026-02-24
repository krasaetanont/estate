from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.models.models import ListingTypeEnum, PropertyStatusEnum, UserRoleEnum


# ─── Location ────────────────────────────────────────────────────────────────

class LocationCreate(BaseModel):
    city: str
    province: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    google_maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationOut(LocationCreate):
    id: int

    class Config:
        from_attributes = True


# ─── Property Photo ───────────────────────────────────────────────────────────

class PhotoCreate(BaseModel):
    url: str
    is_primary: bool = False
    sort_order: int = 0


class PhotoOut(PhotoCreate):
    id: int

    class Config:
        from_attributes = True


# ─── Property ─────────────────────────────────────────────────────────────────

class PropertyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    property_type: Optional[str] = None  # house | apartment | land
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqm: Optional[int] = None
    property_status: PropertyStatusEnum = PropertyStatusEnum.available
    listing_type: ListingTypeEnum = ListingTypeEnum.sale
    rent_period: Optional[str] = None
    location: LocationCreate
    photos: Optional[List[PhotoCreate]] = []


class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqm: Optional[int] = None
    property_status: Optional[PropertyStatusEnum] = None
    listing_type: Optional[ListingTypeEnum] = None
    rent_period: Optional[str] = None


class PropertyOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    property_type: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    area_sqm: Optional[int]
    views_count: int
    property_status: PropertyStatusEnum
    listing_type: ListingTypeEnum
    rent_period: Optional[str]
    owner_id: int
    location: Optional[LocationOut]
    photos: List[PhotoOut] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PropertyListOut(BaseModel):
    id: int
    title: str
    price: float
    property_type: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    area_sqm: Optional[int]
    property_status: PropertyStatusEnum
    listing_type: ListingTypeEnum
    location: Optional[LocationOut]
    photos: List[PhotoOut] = []
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ─── User ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_role: UserRoleEnum = UserRoleEnum.user
    phone_number: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_role: Optional[UserRoleEnum] = None
    phone_number: Optional[str] = None
    is_verified: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    user_role: UserRoleEnum
    phone_number: Optional[str]
    is_verified: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ─── Auth ─────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ─── Pagination ───────────────────────────────────────────────────────────────

class PaginatedProperties(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[PropertyListOut]


class PaginatedUsers(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[UserOut]