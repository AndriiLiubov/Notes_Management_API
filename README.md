
# Notes Management API

## Project Description

This project is an API for managing notes, built using **FastAPI** and **SQLAlchemy**. Users can create, read, update, delete notes, as well as retrieve note versions and their summarized content through integration with **Google Gemini AI**.

## Requirements

- Python 3.10 or above
- Installed libraries:
  - FastAPI
  - Uvicorn
  - SQLAlchemy
  - Pydantic
  - Alembic
  - Google Generative AI (for integration with Gemini AI)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AndriiLiubov/Notes_Management_API
   cd notes-management-api
   ```

2. Create and activate a virtual environment:

   - On Windows:
     ```bash
     python -m venv .venv
     .\.venv\Scriptsctivate
     ```

   - On MacOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory of the project and add your **Google Gemini API key**:

   ```bash
   GENAI_API_KEY=your_google_gemini_api_key
   ```

## Running the Project

To run the application, use the following command:

```bash
uvicorn main:app --host localhost --port 8000 --reload
```

- `uvicorn` — a high-performance ASGI web server;
- `main` — the file `main.py`;
- `app` — the object returned after the request app = FastAPI();
- `--host` — allows binding the socket to a host. The default value is 127.0.0.1;
- `--port` — allows binding the socket to a specific port. The default value is 8000;
- `--reload` — enables hot reloading of the server during development.

After running this, the API will be available at `http://127.0.0.1:8000`.

## Endpoints

### 1. **Create Note**

**POST** `/notes/`

**Request Body**:

```json
{
    "title": "Buy list",
    "content": "Do not forget to buy eggs, milk, bread, apples",
    "created_at": "2025-03-20T10:00:00",
    "updated_at": "2025-03-20T10:00:00"
}
```

### 2. **Get All Notes**

**GET** `/notes/`

**Query Parameters**:
- `skip` (optional) — The number of records to skip for pagination.
- `limit` (optional) — The number of notes to retrieve.

**Response**:

```json
[
  {
    "id": 1,
    "title": "Buy list",
    "content": "Do not forget to buy eggs, milk, bread, apples",
    "created_at": "2025-03-20T10:00:00",
    "updated_at": "2025-03-20T10:00:00"
  }
]
```

### 3. **Get Note by ID**

**GET** `/notes/{note_id}/`

**Response**:

```json
{
  "id": 1,
  "title": "Buy list",
  "content": "Do not forget to buy eggs, milk, bread, apples",
  "created_at": "2025-03-20T10:00:00",
  "updated_at": "2025-03-20T10:00:00"
}
```

### 4. **Update Note**

**PUT** `/notes/{note_id}/`

**Request Body**:

```json
{
  "title": "Updated title",
  "content": "Updated content"
}
```

**Response**:

```json
{
  "message": "Note updated successfully"
}
```

### 5. **Delete Note**

**DELETE** `/notes/{note_id}/`

**Response**:

```json
{
  "message": "Note deleted"
}
```

### 6. **Get Note Versions**

**GET** `/notes/{note_id}/versions/`

**Response**:

```json
[
  {
    "id": 1,
    "note_id": 1,
    "title": "Buy list",
    "content": "Do not forget to buy eggs, milk, bread, apples",
    "created_at": "2025-03-20T10:00:00"
  }
]
```

### 7. **Get Note Summary**

**GET** `/notes/{note_id}/summary/`

**Response**:

```json
{
  "note_id": 1,
  "summary": "Summary of the note content"
}
```

## Testing

For testing the project, use **pytest**. To run the tests, execute the following command:

```bash
pytest
```

Tests verify the creation, reading, updating, and deletion of notes, as well as functionality related to note versions and summaries.

