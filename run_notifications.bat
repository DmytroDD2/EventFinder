@echo off
powershell -WindowStyle Hidden -Command "docker exec my_web_container python /code/app/notifications/auto_create_notifications.py"

