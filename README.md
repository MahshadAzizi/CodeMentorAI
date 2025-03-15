# CodeMentorAI

## Environment Variables

### 1. `.env` File
This file contains configuration for the Backend service, Celery and Database connections.

#### Example `.env` File:
```ini
# Database URLs
DATABASE_URL=postgresql://user:password@host:port/database

# Celery Configuration
CELERY_BROKER_URL=CELERY_BROKER_URL
CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND

```
### 2. `db.env` File
This file contains configuration for the PostgreSQL database.

#### Example `db.env` File:
```ini
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_PORT=POSTGRES_PORT
```

## How to run the app: 
1. Clone the repository:
   ```sh
    $ git clone https://github.com/MahshadAzizi/CodeMentorAI.git
    $ cd CodeMentorAI
    ```
2. Build and run the Docker containers:
   ```sh
    $ docker compose up --build
   ```
