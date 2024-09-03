# Base image
FROM python:3.9

# Set the working directory
WORKDIR /code

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code/

# Use a shell form of CMD to run multiple commands
CMD uvicorn app.main:app --host 0.0.0.0 --port 8080 & streamlit run appui.py --port 80 --server.headless true
