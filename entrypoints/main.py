from fastapi import FastAPI
from app.routes import schedule_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Schedule API",
    version="1.0",
    description="REST API for managing class schedules in Firestore"
)

app.include_router(schedule_routes.router)