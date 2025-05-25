import os
import json
import psycopg2
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder

# Load environment variables
load_dotenv()

# Environment vars (loaded once)
DB_CONFIG = {
    "dbname": os.getenv("SUPABASE_DB"),
    "user": os.getenv("SUPABASE_USER"),
    "password": os.getenv("SUPABASE_PASS"),
    "host": os.getenv("SUPABASE_HOST"),
    "port": "5432",
}


def save_scan_result(data):
    # Convert datetime and other non-serializable types
    encoded_data = jsonable_encoder(data)

    # Open a new DB connection for this operation
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO scans (data) VALUES (%s);",
                [json.dumps(encoded_data)]
            )
            conn.commit()
