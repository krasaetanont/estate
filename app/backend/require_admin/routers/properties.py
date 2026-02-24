from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies.guards import get_current_user, require_seller
from app.models.models import (
    ListingTypeEnum, Location, Property, PropertyPhoto,
    PropertyStatusEnum, User,
)
from app.schemas.schemas import (
    PaginatedProperties, PropertyCreate, PropertyListOut,
    PropertyOut, PropertyUpdate,
)

router = APIRouter(prefix="/api/properties", tags=["Properties"])


def _property_query():
    """Base query with eager-loaded relations."""
    return (
        select(Property)
        .options(
            selectinload(Property.location),
            selectinload(Property.photos),
            selectinload(Property.owner),
        )
    )


# ─── Public: List / Browse ────────────────────────────────────────────────────

@router.get("", response_model=PaginatedProperties)
async def list_properties(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    listing_type: Optional[ListingTypeEnum] = None,
    property_status: Optional[PropertyStatusEnum] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    city: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Browse all properties with optional filters.
    Public endpoint — no auth required.
    """
    query = _property_query()

    if listing_type:
        query = query.where(Property.listing_type == listing_type)
    if property_status:
        query = query.where(Property.property_status == property_status)
    if property_type:
        query = query.where(Property.property_type == property_type)
    if min_price is not None:
        query = query.where(Property.price >= min_price)
    if max_price is not None:
        query = query.where(Property.price <= max_price)
    if city:
        query = query.join(Property.location).where(
            Location.city.ilike(f"%{city}%")
        )

    # Total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Paginated results
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size).order_by(Property.created_at.desc()))
    properties = result.scalars().all()

    return PaginatedProperties(
        total=total,
        page=page,
        page_size=page_size,
        results=[PropertyListOut.model_validate(p) for p in properties],
    )


@router.get("/{property_id}", response_model=PropertyOut)
async def get_property(property_id: int, db: AsyncSession = Depends(get_db)):
    """Get full detail of a single property. Increments view count."""
    result = await db.execute(_property_query().where(Property.id == property_id))
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    # Increment view count
    prop.views_count = (prop.views_count or 0) + 1
    db.add(prop)
    await db.commit()
    await db.refresh(prop)

    return PropertyOut.model_validate(prop)


# ─── Seller: My Listings ──────────────────────────────────────────────────────

@router.get("/seller/my-listings", response_model=PaginatedProperties)
async def my_listings(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db),
):
    """List all properties owned by the authenticated seller."""
    query = _property_query().where(Property.owner_id == current_user.id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size).order_by(Property.created_at.desc()))
    properties = result.scalars().all()

    return PaginatedProperties(
        total=total,
        page=page,
        page_size=page_size,
        results=[PropertyListOut.model_validate(p) for p in properties],
    )


# ─── Seller: Create ───────────────────────────────────────────────────────────

@router.post("", response_model=PropertyOut, status_code=status.HTTP_201_CREATED)
async def create_property(
    body: PropertyCreate,
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new property listing.
    Requires seller or admin role.
    Location and photos are created in the same request.
    """
    # Create location
    location = Location(**body.location.model_dump())
    db.add(location)
    await db.flush()  # get location.id without committing

    # Create property
    prop = Property(
        title=body.title,
        description=body.description,
        price=body.price,
        property_type=body.property_type,
        bedrooms=body.bedrooms,
        bathrooms=body.bathrooms,
        area_sqm=body.area_sqm,
        property_status=body.property_status,
        listing_type=body.listing_type,
        rent_period=body.rent_period,
        owner_id=current_user.id,
        location_id=location.id,
    )
    db.add(prop)
    await db.flush()

    # Create photos
    for photo in body.photos or []:
        db.add(PropertyPhoto(property_id=prop.id, **photo.model_dump()))

    await db.commit()

    # Reload with relations
    result = await db.execute(_property_query().where(Property.id == prop.id))
    return PropertyOut.model_validate(result.scalar_one())


# ─── Seller: Update ───────────────────────────────────────────────────────────

@router.patch("/{property_id}", response_model=PropertyOut)
async def update_property(
    property_id: int,
    body: PropertyUpdate,
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a property listing.
    Seller can only update their own listings; admin can update any.
    """
    result = await db.execute(_property_query().where(Property.id == property_id))
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    from app.models.models import UserRoleEnum
    if prop.owner_id != current_user.id and current_user.user_role != UserRoleEnum.admin:
        raise HTTPException(status_code=403, detail="You can only update your own listings")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)

    db.add(prop)
    await db.commit()

    result = await db.execute(_property_query().where(Property.id == prop.id))
    return PropertyOut.model_validate(result.scalar_one())


# ─── Seller: Delete ───────────────────────────────────────────────────────────

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: int,
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a property listing.
    Seller can only delete their own listings; admin can delete any.
    """
    result = await db.execute(select(Property).where(Property.id == property_id))
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    from app.models.models import UserRoleEnum
    if prop.owner_id != current_user.id and current_user.user_role != UserRoleEnum.admin:
        raise HTTPException(status_code=403, detail="You can only delete your own listings")

    await db.delete(prop)
    await db.commit()