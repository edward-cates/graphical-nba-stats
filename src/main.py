import os
from pathlib import Path
import json

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.db import Db

# Load environment variables from .env.json
env_path = Path('.env.json')
if env_path.exists():
    with open(env_path) as f:
        env_vars = json.load(f)
        for key, value in env_vars.items():
            os.environ[key] = str(value)

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/web"), name="static")

@app.get("/hello-world")
async def hello_world():
    return "hi"


