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
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.databases import crud, models, schemas
from app.databases.database import SessionLocal, engine

from ..dependencies import get_token_header

# router = APIRouter(
#     prefix="/excel",
#     tags=["process excel"],
#     dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )

router = APIRouter(
    prefix="/excel",
    tags=["process excel"],
)

executor = ThreadPoolExecutor()


@router.post('/process_excel')
async def process_excel(request: Request):
    excel_data = await request.body()

    df = pd.read_excel(BytesIO(excel_data))

    grouped_df = df.groupby('ProductType')

    # Create the folder path for output files
    random_num = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    folder_path = f"E:/Dev/Data/Working/{random_num}"
    os.makedirs(folder_path)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = []
        for product_type, group_df in grouped_df:
            task = executor.submit(perform_data_transformation, group_df, folder_path, product_type, random_num)
            tasks.append(task)

        # Wait for all tasks to complete
        concurrent.futures.wait(tasks)

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