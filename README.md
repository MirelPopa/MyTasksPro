# Task Management API

This is a task management backend built with FastAPI, PostgreSQL, Redis, Celery, and Docker. It includes JWT-based authentication, task creation and management, and background task processing with Celery.

## Features

- User signup and login with JWT authentication
- JWT-protected routes for all task operations
- Create, read, update, and delete tasks
- Export tasks to CSV in the background using Celery
- PostgreSQL as the database
- Redis as the Celery broker
- Flower for monitoring background tasks

## Technologies Used

- FastAPI (web framework)
- PostgreSQL (database)
- SQLAlchemy (ORM)
- Redis (message broker for Celery)
- Celery (background job processing)
- Flower (Celery monitoring dashboard)
- JWT / OAuth2PasswordBearer (authentication)
- Docker & Docker Compose (containerization)

## Endpoints

All endpoints are defined in `main.py`. Key routes include:

| Method | Endpoint                  | Description                           |
|--------|---------------------------|---------------------------------------|
| POST   | `/signup`                 | Create a new user                     |
| POST   | `/login`                  | Authenticate a user and get token     |
| GET    | `/me`                     | Get the currently authenticated user  |
| GET    | `/tasks/`                 | List all tasks for the current user   |
| POST   | `/tasks/`                 | Create a new task                     |
| GET    | `/tasks/{item_id}`        | Get a specific task                   |
| PUT    | `/tasks/{item_id}`        | Update a specific task                |
| DELETE | `/tasks/{item_id}`        | Delete a task                         |
| GET    | `/tasks/export-tasks`     | Export all tasks to CSV (background)  |
| GET    | `/export-status/{job_id}` | Get the status of a background export |

## Setup Instructions

### Prerequisite

- Docker installed on your machine

### Steps

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. Open `docker-compose.yml` and update the Postgres volume line:
   Replace this:
   ```yaml
   - C:/Users/Mirel/PycharmProjects/mytasksprodb:/var/lib/postgresql/data
   ```
   with a valid path on your local machine.

3. Open a terminal in the project directory.

4. Run the following command to build and start the containers:
   ```bash
   docker-compose up --build
   ```

### To Reset the Project

Stop all containers and remove the volumes:
```bash
docker-compose down -v
```

### To Start the Project Without Rebuilding

If the containers are already built:
```bash
docker-compose up
```
