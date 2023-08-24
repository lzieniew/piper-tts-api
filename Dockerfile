# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the local app.py file into the container
COPY . .

# Install piper-tts and fastapi
RUN pip install -r requirements.txt

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "rest_api:app", "--host", "0.0.0.0", "--port", "5000"]
