FROM python:3.11-slim

WORKDIR /code

# Copy requirements first for faster building
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder content into /code
COPY backend/ /code/

# Set the environment variable so Python can find the 'src' module
ENV PYTHONPATH=/code

# Run uvicorn pointing exactly to the main.py inside src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]