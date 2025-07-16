from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import admins, employees, roles
from app.database import Base, engine

app = FastAPI(title="Admin & Employee Management")

# ✅ Allow CORS (Frontend React running on Vite)
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # Sometimes Vite uses 127.0.0.1
    # Add production URL here when deploying
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Allows listed origins
    allow_credentials=True,
    allow_methods=["*"],           # Allows all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],           # Allows all headers
)

# ✅ (Optional) Create tables (only for first-time dev, Alembic recommended for migrations)
Base.metadata.create_all(bind=engine)

# ✅ Include routers
app.include_router(admins.router)
app.include_router(employees.router)
app.include_router(roles.router)