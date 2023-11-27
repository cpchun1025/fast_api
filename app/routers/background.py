import asyncio
from typing import Annotated

import aiocron
from fastapi import APIRouter, BackgroundTasks, Depends

router = APIRouter(
    prefix="/background",
    tags=["process background"],
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

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@router.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}