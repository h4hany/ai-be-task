from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .database import engine
from .models import user, book
from .routers import auth, books

# Create database tables
user.Base.metadata.create_all(bind=engine)
book.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Include routers
app.include_router(auth.router)
app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Book Analysis API"} 