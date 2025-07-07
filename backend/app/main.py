from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.db.seed_database import seed_database
from app.utils.file_operations import UPLOAD_DIR
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_database()
    yield

app = FastAPI(docs_url="/docs", redoc_url=None, lifespan=lifespan)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

from app.users import routes as user_routes
from app.events import routes as event_routes
from app.tickets import routes as ticket_routes
from app.reviews import routes as review_routes
from app.friends import routes as friends_routes
from app.notifications import routes as notification_routes

origins = [
    # "http://localhost",
    # "http://localhost:8080",
    # "https://example.com",
    # "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(friends_routes.router, prefix="/users/friends", tags=["friends"]),

app.include_router(event_routes.router, prefix="/events", tags=["events"])
app.include_router(ticket_routes.router, prefix="/tickets", tags=["tickets"])
app.include_router(review_routes.router, prefix="/reviews", tags=["reviews"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["notifications"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



