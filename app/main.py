from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users, db, excel
import app.routers.background

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(db.router)
app.include_router(excel.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


import asyncio

async def process_record(record_id):
    # Simulate calling the external API asynchronously
    await asyncio.sleep(1)
    # Update the record with status = 1
    # Replace this with your actual code to update the record
    print(f"Record {record_id} processed successfully")


async def start_background_task():
    # Simulate fetching records from the database with status = 0
    records = [1, 2, 3, 4, 5]  # Replace this with your actual code to fetch records

    for record_id in records:
        # Process each record asynchronously
        await process_record(record_id)


@app.on_event("startup")
async def startup_event():
    # Start the background task when FastAPI starts
    await start_background_task()
    
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
