from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, properties, users

app = FastAPI(
    title="Real Estate API",
    description="Backend API for a real estate listing platform.",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Real Estate API is running"}