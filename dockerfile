FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Run create_faker_events.py and then start uvicorn server
CMD ["sh", "-c", "python sources/create_faker_events.py && uvicorn main:app --host=0.0.0.0 --port=9000 --log-level=info --reload"]
