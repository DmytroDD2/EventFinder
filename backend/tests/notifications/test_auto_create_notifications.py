# import pytest
#
# from app.events.models import Event
# from app.notifications.auto_create_notifications import create_notifications_for_upcoming_events
# from app.notifications.models import Notification
# from app.tickets.models import Tickets
# from ..utils import test_user_tickets, test_user
# import pytest
# from datetime import datetime, timedelta
#
# @pytest.mark.asyncio
# async def test_create_notifications_for_upcoming_events(client, test_db, test_user_tickets, test_user):
#
#     create_notifications_for_upcoming_events(test_db)
#     response = client.get("/users/notifications", headers={"Authorization": "Bearer valid_token"})
#     assert response.status_code == 200
