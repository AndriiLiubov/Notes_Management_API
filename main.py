from fastapi import FastAPI
from src.routes import notes

app = FastAPI()

app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "Welcome to Notes Manager"}

# uvicorn main:app --host localhost --port 8000 --reload
