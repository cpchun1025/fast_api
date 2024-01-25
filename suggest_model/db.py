from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()

class PreProcessData(Base):
    __tablename__ = "preprocessdata"
    id = Column(Integer, primary_key=True, index=True)
    field1 = Column(String)
    field2 = Column(String)
    # ... define all 12 fields as needed

class ProcessedData(Base):
    __tablename__ = "processeddata"
    id = Column(Integer, primary_key=True, index=True)
    field1 = Column(String)
    field2 = Column(String)
    # ... define all fields again, or possibly include a processing status or results

# Create the database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)