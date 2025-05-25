from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from .aws_scanner import scan_all
from .db import save_scan_result
from cwpp.runtime_scanner import run_runtime_checks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess
import json
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CSPM Scan Endpoint
@app.get("/scan/cspm")
def scan_cspm():
    results = scan_all()
    save_scan_result(results)
    encoded_results = jsonable_encoder(results)
    return {"status": "ok", "results": encoded_results}

# CWPP Scan Endpoint
@app.get("/scan/cwpp")
def scan_cwpp():
    results = run_runtime_checks()
    save_scan_result(results)  # stores in Supabase
    encoded_results = jsonable_encoder(results)
    return {"status": "ok", "results": encoded_results}

# Steampipe Query Endpoint
@app.get("/steampipe/results")
def steampipe_results():
    query = "select * from aws_iam_user limit 5;"  # Replace with any valid query
    try:
        completed_process = subprocess.run(
            ['/usr/local/bin/steampipe', 'query', '--json', query],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        results = json.loads(completed_process.stdout)
        return {"status": "ok", "results": results}
    except subprocess.CalledProcessError as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": e.stderr}
        )

# Local dev runner
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
