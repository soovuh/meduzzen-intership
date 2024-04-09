from fastapi import FastAPI
from dotenv import load_dotenv

# load environment variables
load_dotenv()

app = FastAPI()


@app.get("/")
def health_check():
    """Perform a basic app check."""
    return {"status": 200, "detail": "ok", "result": "working"}
