FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install fastapi boto3 psycopg2-binary uvicorn python-dotenv

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
