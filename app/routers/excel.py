import asyncio
import csv
import random
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

    # Read the Excel file as a pandas DataFrame
    df = pd.read_excel(BytesIO(excel_data))

    # Perform data transformation asynchronously
    transformed_df = await asyncio.get_event_loop().run_in_executor(
        executor, perform_data_transformation, df
    )

    # Convert the transformed DataFrame to a CSV string
    csv_string = transformed_df.to_csv(index=False)

    # Create an in-memory byte stream from the CSV string
    output = BytesIO()
    output.write(csv_string.encode("utf-8"))
    output.seek(0)

    # Return the byte stream as a streaming response with the appropriate headers
    return StreamingResponse(
        output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=processed_file.csv"}
    )


def perform_data_transformation(df):
    # Perform your actual data transformation logic here
    # This function will run in a separate thread

    # Perform your processing on the dataframe
    # Replace this with your actual processing logic
    # Here, we are simply doubling the values in the 'Value' column
    df['vv'] = df['vv'] + " process"
    
    # For example, let's add a new column with transformed values
    df['TransformedValue'] = df['Value'] * 2

    # Simulate some computational delay
    # asyncio.sleep()  # Note: Removed the "await" keyword here
    
    print(df)    
    time.sleep(random.randrange(0,10))
    print("done")
    return df