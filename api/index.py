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

# Load the JSON data
try:
    json_path = os.path.join(os.path.dirname(__file__), "q-versel-python.json")
    with open(json_path, "r") as f:
        data = json.load(f)
    marks_dict = {entry["name"]: entry["marks"] for entry in data}
    print(f"✅ Loaded {len(marks_dict)} students")
    print(f"🔍 Available names: {list(marks_dict.keys())}")  # Log available names
except Exception as e:
    print(f"❌ Failed to load JSON: {e}")

@app.get("/api")
async def get_marks(request: Request):
    names = request.query_params.getlist("name")
    print(f"🔍 Query for names: {names}")  # Log the query parameters
    result = [marks_dict.get(name, None) for name in names]
    print(f"✅ Result for names: {result}")  # Log the result to debug
    return JSONResponse(content={"marks": result})
