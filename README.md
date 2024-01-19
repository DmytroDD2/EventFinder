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
     # Optional: To enable email notifications, provide email credentials.
     # Note: You can leave these fields empty or not specify them at all, as they are optional.
     # If provided, the application will send a reset token to the specified email address when a password reset is requested.
     # If these fields are left empty or unspecified, the application will handle password reset without sending an email notification.

     MAIL_USERNAME=your_email@gmail.com
     MAIL_APP_PASSWORD=your_secure_password_here
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up a Virtual Environment:**
    - Before installing the project dependencies, it's recommended to create a virtual environment:
      ```bash
      python -m venv myenv
      source myenv/bin/activate  # On Windows, use: myenv\Scripts\activate
      ```

5. **Run using Docker:**
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
  - In the "Program/script" field, enter the path to your .bat file. For example:
  - In the "Program/script" field, enter the path to your .bat file. For example:
    `C:\Users\YourUsername\Documents\EventFinder\run_notifications.bat`
  - In the "Start in (optional)" field, enter the directory where your Python script should run. For example:
     `C:\Users\YourUsername\Documents\EventFinder`
  - Finish the setup process.
  
Once the task is added, it will run the specified .bat file at the scheduled time, automating the process within your Event Finder Application.
