import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

marks_dict = {}

# Correct the path to the JSON file and add logging for errors
json_path = os.path.join(os.path.dirname(__file__), "q-versel-python.json")

# Check if the file exists at the path
if os.path.exists(json_path):
    print(f"✅ JSON file found at: {json_path}")
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        marks_dict = {entry["name"]: entry["marks"] for entry in data}
        print(f"✅ Loaded {len(marks_dict)} students")
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
else:
    print(f"❌ JSON file not found at: {json_path}")

@app.get("/api")
async def get_marks(request: Request):
    names = request.query_params.getlist("name")
    print(f"🔍 Query for names: {names}")
    result = [marks_dict.get(name, None) for name in names]
    print(f"✅ Result for names: {result}")
    return JSONResponse(content={"marks": result})
