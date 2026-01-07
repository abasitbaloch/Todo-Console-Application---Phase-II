FROM python:3.11-slim

# Step 1: Set the working directory to the backend folder
WORKDIR /code/backend

# Step 2: Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Copy all files from the local backend folder into the container's working directory
COPY backend/ .

# Step 4: Run uvicorn. Since we are already inside /code/backend, 
# and main.py is in src/, we use src.main:app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]