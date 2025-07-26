# Event Finder Application

This project is a full-stack API application that allows users to create and search for events, register for them, leave reviews, and much more.

## Technologies Used

- **Frontend: React, TypeScript, HTML, CSS Modules, Zustand, React Motion, Yarn 
- **Backend:** FastAPI, PostgreSQL, Alembic, Celery, RabbitMQ  
- **Testing:** Pytest (async support, coverage: **89%**)   
- **Docker & Docker Compose:** For containerized local developmen

---

## Installation and Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/DmytroDD2/EventFinder.git
    cd EventFinder
    ```

2. **Create a `.env` file** with the following content:

    ```env
     # Optional: To enable email notifications, provide email credentials.
     # Note: You can leave these fields empty or not specify them at all, as they are optional.
     # If provided, the application will send a reset token to the specified email address when a password reset is requested.
     # If these fields are left empty or unspecified, the application will handle password reset without sending an email notification.

     MAIL_USERNAME=your_email@gmail.com
     MAIL_APP_PASSWORD=your_secure_password_here
    ```

3. **Run using Docker:**
    ```bash
    docker compose up --build
    ```
    This will start:

     - PostgreSQL database  
     - RabbitMQ message broker  
     - Backend API server (FastAPI + Uvicorn)  
     - Frontend app (React)  
     - Celery worker  
   
   > **Note:** On the first run (after migrations), the database will be automatically seeded with initial test data.  
   > This is handled by a seeding script inside the backend which creates example users, events, and other necessary records.
---


## Scheduled Tasks

The application uses Celery Beat to schedule periodic tasks, such as sending daily notifications for upcoming events. Celery Beat automatically triggers these tasks at the specified time intervals defined in your Celery configuration. No manual setup (such as Windows Task Scheduler) is required.

## Frontend

Once the project is running, the frontend application will be available at:  
[http://localhost:80](http://localhost:3000)

## API Documentation

After running the project, you can view the interactive API docs (Swagger UI) at:  
[http://localhost:8000/docs](http://localhost:8000/docs)




## Run Backend Tests

To run backend tests inside the Docker container:
   
   ```bash
   docker compose up -d test_db && \
   sleep 3 && \
   docker compose run --rm backend pytest --cov && \
   docker compose down
   ```
   
   This will:

      - Start the test_db container
      
      - Wait a few seconds to ensure DB is ready
      
      - Run pytest with code coverage
      
      - Shut everything down after tests complete
      
   🔍 Latest test coverage: 89%
---