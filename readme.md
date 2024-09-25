# FastAPI Event Management Backend

This is a FastAPI backend application for managing events, built using FastAPI and Supabase for database management. It allows users to create, read, update, and delete events.

## Features

- Create new events
- Retrieve all events
- Retrieve a specific event by ID
- Update existing events

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.7+.
- **Supabase**: A backend-as-a-service that provides a PostgreSQL database.
- **Python**: The programming language used for this application.
- **dotenv**: For managing environment variables.

## Prerequisites

- Python 3.7 or higher
- Supabase account
- PostgreSQL database (managed by Supabase)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/robertsibanda/event_management_system.git
   cd your-repo-name

   python -m venv venv

   venv\Scripts\activate

   source venv/bin/activate

   pip install fastapi[all] python-dotenv supabase


**Set up your environment variables:**

Create a .env file in the root directory of your project with the following content:

```SUPABASE_URL=your_supabase_url    SUPABASE_KEY=your_supabase_key ```



Replace your_supabase_url and your_supabase_key with your actual Supabase credentials.

**To start the FastAPI server, run:**

```uvicorn main:app --reload ```

Open your browser and go to http://localhost:8000/docs to access the automatic Swagger documentation for the API.
