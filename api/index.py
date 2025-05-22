from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

marks_dict = {}

try:
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "q-versel-python.json"))
    print(f"Loading JSON from: {json_path}")
    with open(json_path, "r") as f:
        data = json.load(f)
    marks_dict = {entry["name"]: entry["marks"] for entry in data}
    print(f"Loaded {len(marks_dict)} records.")
except Exception as e:
    print(f"❌ Error loading marks file: {e}")

@app.get("/api")
async def get_marks(request: Request):
    names = request.query_params.getlist("name")
    print(f"Received query for names: {names}")
    result = [marks_dict.get(name, None) for name in names]
    return JSONResponse(content={"marks": result})
