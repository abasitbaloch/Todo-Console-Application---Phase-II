# Use Python 3.11
FROM python:3.11

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file first (to cache dependencies)
COPY ./backend/requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the backend code
COPY ./backend /code

# Create a non-root user (Hugging Face requires this for security)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Hugging Face expects the app to run on port 7860
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "7860"]