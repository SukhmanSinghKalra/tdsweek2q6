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

json_path = os.path.join(os.path.dirname(__file__), "../q-versel-python.json")
with open(json_path, "r") as f:
    data = json.load(f)

marks_dict = {entry["name"]: entry["marks"] for entry in data}

@app.get("/api")
async def get_marks(request: Request):
    names = request.query_params.getlist("name")
    result = [marks_dict.get(name, None) for name in names]
    return JSONResponse(content={"marks": result})
