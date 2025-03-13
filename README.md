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
