from fastapi import FastAPI
from dotenv import load_dotenv

from routers.main_router import router

# load environment variables
load_dotenv()

app = FastAPI()

# Include main router
app.include_router(router, prefix="")
