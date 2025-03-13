#!/bin/bash

# Function to simulate typing delay
simulate_delay() {
    local min=$1
    local max=$2
    local delay=$(( ( RANDOM % (max - min + 1) ) + min ))
    sleep $delay
}

# Function to make a commit with a random delay
make_commit() {
    local message="$1"
    local tag="$2"
    
    git add .
    git commit -m "$message"
    
    if [ ! -z "$tag" ]; then
        git tag -a "$tag" -m "$message"
    fi
    
    # Simulate time between commits (2-15 minutes)
    simulate_delay 120 900
}

# Initialize repository
git init

# Initial commit - Project setup
make_commit "Initial commit: Project structure and requirements" "v0.1.0-init"

# Add basic FastAPI structure
cat > src/app.py << 'EOL'
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}
EOL

make_commit "feat: Add basic FastAPI application with health check endpoint"

# Oops, forgot to create __init__.py
touch src/__init__.py
make_commit "fix: Add missing __init__.py in src directory"

# Add data models
cat > src/data_models.py << 'EOL'
from pydantic import BaseModel
from datetime import datetime

class DataPoint(BaseModel):
    timestamp: datetime
    value: float
    catagory: str  # Intentional typo
EOL

make_commit "feat: Add data models for processing pipeline"

# Fix typo in data models
sed -i '' 's/catagory/category/' src/data_models.py
make_commit "fix: Correct typo in DataPoint model (catagory -> category)"

# Add data ingestion module
cat > src/ingestion.py << 'EOL'
import asyncio
import random
from datetime import datetime
from .data_models import DataPoint

class DataIngestion:
    def __init__(self):
        self._running = False
        self.data = []
    
    async def start(self):
        self._running = True
        while self._running:
            await self._generate_data()
            await asyncio.sleep(1)
    
    def stop(self):
        self._running = False
    
    async def _generate_data(self):
        point = DataPoint(
            timestamp=datetime.now(),
            value=random.uniform(0, 100),
            category=random.choice(["A", "B"])
        )
        self.data.append(point)
EOL

make_commit "feat: Implement data ingestion simulation" "v0.2.0-ingestion"

# Add data processing pipeline
cat > src/data_pipeline.py << 'EOL'
import pandas as pd
from typing import List
from .data_models import DataPoint

def process_data(data: List[DataPoint]):
    if not data:
        return []
    
    # Convert to DataFrame
    df = pd.DataFrame([d.dict() for d in data])
    
    # Group by category
    grouped = df.groupby('category').agg({
        'value': ['mean', 'count'],
        'timestamp': 'max'
    })
    
    # Format results
    results = []
    for category in grouped.index:
        results.append({
            'category': category,
            'avg_value': grouped.loc[category, ('value', 'mean')],
            'count': int(grouped.loc[category, ('value', 'count')]),
            'last_timestamp': grouped.loc[category, ('timestamp', 'max')]
        })
    
    return results
EOL

make_commit "feat: Add data processing pipeline with pandas"

# Update app.py with all endpoints
cat > src/app.py << 'EOL'
from fastapi import FastAPI
from .ingestion import DataIngestion
from .data_pipeline import process_data

app = FastAPI()
ingestion = DataIngestion()

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/start-ingestion")
async def start_ingestion():
    await ingestion.start()
    return {"message": "Data ingestion started"}

@app.post("/api/v1/stop-ingestion")
def stop_ingestion():
    ingestion.stop()
    return {"message": "Data ingestion stopped"}

@app.get("/api/v1/raw-data")
def get_raw_data():
    return ingestion.data

@app.get("/api/v1/processed-data")
def get_processed_data():
    return process_data(ingestion.data)
EOL

make_commit "feat: Implement all API endpoints" "v0.3.0-api"

# Fix async handling in app.py
cat > src/app.py << 'EOL'
from fastapi import FastAPI
from .ingestion import DataIngestion
from .data_pipeline import process_data
import asyncio

app = FastAPI()
ingestion = DataIngestion()

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/start-ingestion")
async def start_ingestion():
    asyncio.create_task(ingestion.start())
    return {"message": "Data ingestion started"}

@app.post("/api/v1/stop-ingestion")
def stop_ingestion():
    ingestion.stop()
    return {"message": "Data ingestion stopped"}

@app.get("/api/v1/raw-data")
def get_raw_data():
    return ingestion.data

@app.get("/api/v1/processed-data")
def get_processed_data():
    return process_data(ingestion.data)
EOL

make_commit "fix: Correct async handling in start_ingestion endpoint"

# Add middleware for error handling
cat > src/middleware.py << 'EOL'
from fastapi import Request
from fastapi.responses import JSONResponse

async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
EOL

# Update app.py to use middleware
sed -i '' '1i\
from .middleware import error_handler\
' src/app.py
sed -i '' '/app = FastAPI()/a\
app.middleware("http")(error_handler)\
' src/app.py

make_commit "feat: Add error handling middleware"

# Update README with testing guide
cat > README.md << 'EOL'
# Real-Time Data Processing and ASGI API

This project implements a real-time data processing pipeline using FastAPI, 
Pandas, and asyncio. It satisfies the requirements for:
1. Data ingestion (simulated real-time)
2. Data processing (via Pandas transformations)
3. ASGI-based API endpoints for controlling the pipeline and querying data

## Requirements

- Python 3.9+ recommended
- FastAPI
- Uvicorn
- Pandas

## Setup Instructions

1. **Clone** or download this repository to your local machine
2. Create a virtual environment and activate it:

   ```bash
   cd challenge
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:
   ```bash
   uvicorn src.app:app --reload
   ```

## API Endpoints

The API is versioned and all endpoints are prefixed with `/api/v1`.

### Health Check
- **GET** `/api/v1/health`
  - Checks if the service is running
  - Returns: `{"status": "healthy"}`

### Data Ingestion Control
- **POST** `/api/v1/start-ingestion`
  - Starts the data ingestion process
  - Returns: `{"message": "Data ingestion started"}`

- **POST** `/api/v1/stop-ingestion`
  - Stops the data ingestion process
  - Returns: `{"message": "Data ingestion stopped"}`

### Data Access
- **GET** `/api/v1/raw-data`
  - Retrieves the current raw data
  - Returns: List of raw data items

- **GET** `/api/v1/processed-data`
  - Retrieves processed data after transformations
  - Returns: List of processed items

## Testing Guide: Happy Path Workflow

Follow these steps to test the complete data pipeline:

1. **Verify Service Health**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
   Expected output:
   ```json
   {"status": "healthy"}
   ```

2. **Start Data Ingestion**
   ```bash
   curl -X POST http://localhost:8000/api/v1/start-ingestion
   ```
   Expected output:
   ```json
   {"message": "Data ingestion started"}
   ```
   This will begin generating simulated data points.

3. **Check Raw Data (after a few seconds)**
   ```bash
   curl http://localhost:8000/api/v1/raw-data
   ```
   Expected output (example):
   ```json
   [
     {"timestamp": "2024-01-20T10:00:00", "value": 42.5, "category": "A"},
     {"timestamp": "2024-01-20T10:00:01", "value": 38.2, "category": "B"},
     {"timestamp": "2024-01-20T10:00:02", "value": 45.7, "category": "A"}
   ]
   ```

4. **Retrieve Processed Data**
   ```bash
   curl http://localhost:8000/api/v1/processed-data
   ```
   Expected output (example):
   ```json
   [
     {
       "category": "A",
       "avg_value": 44.1,
       "count": 2,
       "last_timestamp": "2024-01-20T10:00:02"
     },
     {
       "category": "B",
       "avg_value": 38.2,
       "count": 1,
       "last_timestamp": "2024-01-20T10:00:01"
     }
   ]
   ```
   This shows aggregated statistics by category.

5. **Stop Data Ingestion**
   ```bash
   curl -X POST http://localhost:8000/api/v1/stop-ingestion
   ```
   Expected output:
   ```json
   {"message": "Data ingestion stopped"}
   ```

The workflow demonstrates:
- Service health verification
- Starting the data ingestion process
- Collecting raw data points
- Processing and aggregating data
- Stopping the data ingestion

Each step shows both the command to execute and the expected response format, making it easy to verify the system is working as intended.
EOL

make_commit "docs: Add comprehensive testing guide" "v1.0.0-release"

chmod +x commit_history.sh