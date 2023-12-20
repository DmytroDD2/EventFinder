from fastapi import FastAPI

app = FastAPI(docs_url="/docs", redoc_url=None)


from app.users import routes as user_routes
from app.events import routes as event_routes
from app.tickets import routes as ticket_routes
from app.reviews import routes as review_routes
from app.notifications import routes as notification_routes

# Include the routes from other modules
app.include_router(user_routes.router, prefix="/users", tags=["users"])
# app.include_router(user_routes.router, prefix="/token", tags=["token"])
# app.include_router(user_routes.router, prefix="", tags=["register"])
app.include_router(event_routes.router, prefix="/events", tags=["events"])
app.include_router(ticket_routes.router, prefix="/tickets", tags=["tickets"])
app.include_router(review_routes.router, prefix="/events/{event_id}/review", tags=["reviews"])
app.include_router(notification_routes.router, prefix="/users/notifications", tags=["notifications"])

from app.db import session



# @app.on_event("startup")
# async def startup_db_client():
#     await engine.connect()
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     await engine.disconnect()