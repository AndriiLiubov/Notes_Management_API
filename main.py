from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Notes Manager"}

# uvicorn main:app --host localhost --port 8000 --reload
