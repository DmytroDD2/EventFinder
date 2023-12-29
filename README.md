# Event Finder Application

This project is an API application that allows users to create and search for events, register for them, leave reviews, and much more.

## Installation and Setup

1. **Clone the repository:**
    ```bash
    git clone [repository URL]
    cd EventFinderApplication
    ```

2. **Create a `.env` file** with the following content:
    ```env
    MAIL_USERNAME_ENV=your_email@gmail.com
    MAIL_APP_PASSWORD_ENV=your_secure_password_here
    DATABASE_URL=postgresql://your_user:your_password@db/your_db_name
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure PostgreSQL:**
    - **Using Docker:**
      Update your `docker-compose.yml` file to include the PostgreSQL environment variables:
      ```yaml
      services:
        db:
          image: postgres
          restart: always
          environment:
            POSTGRES_PASSWORD: your_password
            POSTGRES_USER: your_user
            POSTGRES_DB: your_db_name
          ports:
            - "[HOST_PORT]:[CONTAINER_PORT]" # Replace HOST_PORT and CONTAINER_PORT as needed
      ```

5. **Set up a Virtual Environment:**
    - Before installing the project dependencies, it's recommended to create a virtual environment:
      ```bash
      python -m venv myenv
      source myenv/bin/activate  # On Windows, use: myenv\Scripts\activate
      ```

6. **Run using Docker:**
    ```bash
    docker-compose up --build
    ```

## Documentation

After running the project, you can view the documentation at: `http://localhost:8000/docs`.

## Scheduled Tasks on Windows

To automate the process of generating notifications for upcoming events, which involves querying the database for events scheduled for the next day and then creating notifications based on that data, you can use the Windows Task Scheduler.

- **Add Task to Task Scheduler:**
  - Open the Windows Task Scheduler.
  - Navigate to "Create Basic Task" in the right panel.
  - Provide a name and description for your task.
  - Set the desired trigger (e.g., daily, weekly, etc.).
  - Select "Start a program" as the action.
  - In the "Program/script" field, browse and select the docker executable (usually located at `C:\Program Files\Docker\Docker\resources\bin\docker.exe` or similar).
  - In the "Add arguments" field, enter `exec my_web_container python /code/app/notifications/auto_create_notifications.py`.
  - Finish the setup process.
  
Once the task is added, it will run the specified command at the scheduled time, automating the process within your Event Finder Application.
