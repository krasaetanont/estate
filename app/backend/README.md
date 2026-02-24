# Real Estate API

FastAPI backend for a real estate listing platform.

## Tech Stack
- **FastAPI** – web framework
- **SQLAlchemy 2 (async)** – ORM with asyncpg
- **PostgreSQL** – database
- **Pydantic v2** – request/response validation
- **Passlib / bcrypt** – password hashing
- **Python-JOSE** – JWT authentication

---

## Project Structure

```
real-estate-api/
├── app/
│   ├── main.py               # FastAPI app, CORS, routers
│   ├── config.py             # Settings from .env
│   ├── database.py           # Async SQLAlchemy engine & session
│   ├── models/
│   │   └── models.py         # ORM models (User, Property, Location, …)
│   ├── schemas/
│   │   └── schemas.py        # Pydantic request/response schemas
│   ├── dependencies/
│   │   ├── auth.py           # JWT helpers, password hashing
│   │   └── guards.py         # get_current_user, require_seller, require_admin
│   └── routers/
│       ├── auth.py           # POST /api/auth/login
│       ├── properties.py     # Property CRUD endpoints
│       └── users.py          # User CRUD endpoints (admin)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

```bash
# 1. Clone & install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your Postgres credentials and a strong SECRET_KEY

# 3. Run database migrations (apply your database.sql to Postgres first)
psql -U postgres -d realestate -f database.sql

# 4. Start the server
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | Login → returns JWT token |

### Properties (public)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/properties` | List & filter all properties |
| GET | `/api/properties/{id}` | Get property detail (increments view count) |

### Properties (seller 🔒)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/properties/seller/my-listings` | My own listings |
| POST | `/api/properties` | Create a new listing |
| PATCH | `/api/properties/{id}` | Update own listing |
| DELETE | `/api/properties/{id}` | Delete own listing |

### Users (admin 🔒)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/users` | List all users (paginated, filterable by role) |
| GET | `/api/users/{id}` | Get user by ID |
| POST | `/api/users` | Create user |
| PATCH | `/api/users/{id}` | Update user (role, verified, etc.) |
| DELETE | `/api/users/{id}` | Delete user |
| GET | `/api/users/me/profile` | Get own profile (any auth'd user) |

---

## Role System

| Role | Can do |
|------|--------|
| `user` | Browse properties, save favorites (future) |
| `seller` | All of user + create/edit/delete **own** listings |
| `admin` | All of seller + manage all listings + manage all users |

---

## Query Filters for `GET /api/properties`

| Param | Type | Example |
|-------|------|---------|
| `listing_type` | `sale` \| `rent` | `?listing_type=rent` |
| `property_status` | `available` \| `sold` \| `pending` | `?property_status=available` |
| `property_type` | string | `?property_type=apartment` |
| `min_price` | number | `?min_price=500000` |
| `max_price` | number | `?max_price=2000000` |
| `city` | string | `?city=Manila` |
| `page` | int | `?page=2` |
| `page_size` | int | `?page_size=12` |

---

## Example: Create Property (Seller)

```json
POST /api/properties
Authorization: Bearer <token>

{
  "title": "Modern 2BR Condo in BGC",
  "description": "Fully furnished, city view.",
  "price": 15000,
  "property_type": "apartment",
  "bedrooms": 2,
  "bathrooms": 1,
  "area_sqm": 65,
  "listing_type": "rent",
  "rent_period": "month",
  "location": {
    "city": "Taguig",
    "province": "Metro Manila",
    "country": "Philippines",
    "postal_code": "1634",
    "latitude": 14.5547,
    "longitude": 121.0509
  },
  "photos": [
    { "url": "https://example.com/photo1.jpg", "is_primary": true, "sort_order": 0 },
    { "url": "https://example.com/photo2.jpg", "is_primary": false, "sort_order": 1 }
  ]
}
```