import enum
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, Enum, ForeignKey, Integer,
    Numeric, String, Text, Timestamp, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class PropertyStatusEnum(str, enum.Enum):
    available = "available"
    sold = "sold"
    pending = "pending"


class UserRoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"
    seller = "seller"


class ListingTypeEnum(str, enum.Enum):
    sale = "sale"
    rent = "rent"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.user)
    password_hash = Column(Text, nullable=False)
    phone_number = Column(Text)
    is_verified = Column(Boolean, default=False)
    created_at = Column(Timestamp, server_default=func.now())

    properties = relationship("Property", back_populates="owner")
    favorites = relationship("Favorite", back_populates="user")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(Text, nullable=False)
    province = Column(Text)
    country = Column(Text, nullable=False)
    postal_code = Column(Text)
    google_maps_link = Column(Text)
    latitude = Column(Numeric)
    longitude = Column(Numeric)

    properties = relationship("Property", back_populates="location")


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    price = Column(Numeric, nullable=False)
    property_type = Column(Text)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqm = Column(Integer)
    views_count = Column(Integer, default=0)
    property_status = Column(Enum(PropertyStatusEnum), default=PropertyStatusEnum.available)
    listing_type = Column(Enum(ListingTypeEnum), default=ListingTypeEnum.sale)
    rent_period = Column(Text)

    owner_id = Column(Integer, ForeignKey("users.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))

    created_at = Column(Timestamp, server_default=func.now())
    updated_at = Column(Timestamp, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="properties")
    location = relationship("Location", back_populates="properties")
    photos = relationship("PropertyPhoto", back_populates="property", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="property", cascade="all, delete-orphan")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "property_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"))
    created_at = Column(Timestamp, server_default=func.now())

    user = relationship("User", back_populates="favorites")
    property = relationship("Property", back_populates="favorites")


class PropertyPhoto(Base):
    __tablename__ = "property_photos"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"))
    url = Column(Text, nullable=False)
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    property = relationship("Property", back_populates="photos")