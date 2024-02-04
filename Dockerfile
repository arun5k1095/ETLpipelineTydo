# Use Python 3.9 runtime env as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python packages
RUN pip install -r requirements.txt

# Copy the Python script and credentials file into the container
COPY main.py .
COPY Gcloud_Creds_test_user.json .

# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/Gcloud_Creds_test_user.json

# Run the app
CMD ["python", "main.py"]
