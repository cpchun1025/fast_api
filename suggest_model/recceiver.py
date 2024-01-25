from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import ProcessedData, PreProcessData, SessionLocal

# Create the FastAPI app
app = FastAPI()

# Pydantic models for request and response
class DataItem(BaseModel):
    field1: str
    field2: str
    # ... add all fields

# Processed data item, including results
class ProcessedItem(DataItem):  # Inherits all fields from DataItem
    processed_result1: str
    processed_result2: int
    # ... add all additional fields that represent the processed results
    
# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/process/")
def process_data(item: DataItem, db: Session = Depends(get_db)):
    # Add the item to the pre-process table
    db_item = PreProcessData(**item.dict())
    db.add(db_item)
    db.commit()

    try:
        # Process data here and create a new ProcessedData object
        processed_data = ProcessedData(**item.dict())  # This should include your processing logic
        # ... processing logic goes here

        db.add(processed_data)
        db.commit()
        db.refresh(processed_data)

        return {"status": "success", "data": processed_data}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))