from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load marks from JSON file into a dictionary
with open(os.path.join(os.path.dirname(__file__), "../q-versel-python .json")) as f:
    data = json.load(f)
marks_dict = {entry["name"]: entry["marks"] for entry in data}

@app.get("/api")
async def get_marks(request: Request):
    names = request.query_params.getlist("name")
    result = [marks_dict.get(name, None) for name in names]
    return JSONResponse(content={"marks": result})
