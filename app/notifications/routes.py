from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.users.schemas import UserToken
from app.users.security import get_current_user_token
from app.notifications.crud import get_all_notifications, get_notification, get_all_read_notifications

router = APIRouter()


@router.get("", status_code=200)
async def get_all_notification(db: Session = Depends(get_db),
                               user: UserToken = Depends(get_current_user_token)):

    return get_all_notifications(db, user.id)


@router.get("/read", status_code=200)
async def get_read_notification(db: Session = Depends(get_db),
                                user: UserToken = Depends(get_current_user_token)):

    return get_all_read_notifications(db, user.id, True)


@router.get("/unread", status_code=200)
async def get_unread_notification(db: Session = Depends(get_db),
                                  user: UserToken = Depends(get_current_user_token)):

    return get_all_read_notifications(db, user.id, False)


@router.get("/{notification_id}", status_code=200)
async def get_all_event(notification_id: int,
                        db: Session = Depends(get_db),
                        user: UserToken = Depends(get_current_user_token)):

    return get_notification(db, notification_id, user.id)






