import asyncio
import concurrent.futures
import csv
import os
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import pandas as pd
from fastapi import (APIRouter, BackgroundTasks, Depends, FastAPI,
                     HTTPException, UploadFile)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.databases import crud, models, schemas
from app.databases.database import SessionLocal, engine

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/excel",
    tags=["process excel"],
)

background_router = APIRouter(
    prefix="/background",
    tags=["background service"],
)

executor = ThreadPoolExecutor()

@router.post('/process_excel')
async def process_excel(request: Request, background_tasks: BackgroundTasks):
    excel_data = await request.body()

    df = pd.read_excel(BytesIO(excel_data))

    grouped_df = df.groupby('ProductType')

    # Create the folder path for output files
    random_num = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    folder_path = f"E:/Dev/Data/Working/{random_num}"
    os.makedirs(folder_path)

    for product_type, group_df in grouped_df:
        # Schedule the data transformation task in the background
        background_tasks.add_task(perform_data_transformation, group_df, folder_path, product_type, random_num)

    # Return the folder path containing all output files
    return folder_path

def perform_data_transformation(df, folder_path, product_type, random_num):
    # Perform your actual data transformation logic here

    # Create a new DataFrame for each task
    transformed_df = df.copy()

    # Perform your processing on the dataframe
    transformed_df['Value'] = transformed_df['Value'] * 2

    # Save the transformed DataFrame as an XLSX file
    xlsx_file_path = os.path.join(folder_path, f"{product_type}_processed_{random_num}.xlsx")
    transformed_df.to_excel(xlsx_file_path, index=False)

    # Simulate some computational delay
    time.sleep(random.randrange(0, 10))

def perform_data_processing(file_path):
    # Perform your data processing logic here
    # For example, you can read the Excel file and process its data

    # Load the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Perform your data processing operations on the DataFrame
    # ...

    # Simulate some computational delay
    time.sleep(random.randrange(0, 10))

    # Example: Save the processed DataFrame to a new Excel file
    random_num = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    output_file_path = f"/path/to/output/{random_num}_processed.xlsx"
    df.to_excel(output_file_path, index=False)

@router.post('/upload')
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    # Generate a unique filename for the uploaded file
    random_num = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_path = f"/path/to/uploads/{random_num}_{file.filename}"

    # Save the uploaded file to disk
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    # Schedule the data processing task in the background
    background_tasks.add_task(perform_data_processing, file_path)

    # Return a successful response to the VBA client
    return {'status': 'ok'}