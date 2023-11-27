import asyncio
import aiocron
from fastapi import APIRouter

router = APIRouter(
    prefix="/background",
    tags=["process excel"],
)

async def my_task():
    # Perform your task here
    print("Running my_task")


@aiocron.crontab("*/5 * * * *")  # Run every 5 seconds
async def scheduled_task():
    await my_task()


@router.on_event("startup")
async def startup_event():
    # Start the cron scheduler
    aiocron.start()  # Starts all scheduled tasks


@router.on_event("shutdown")
async def shutdown_event():
    # Stop the cron scheduler
    aiocron.stop()  # Stops all scheduled tasks


@router.get("/")
async def root():
    return {"message": "Hello, World!"}