import os
from pathlib import Path
import json

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from src.db import Db

# Load environment variables from .env.json
env_path = Path('.env.json')
if env_path.exists():
    with open(env_path) as f:
        env_vars = json.load(f)
        for key, value in env_vars.items():
            os.environ[key] = str(value)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="src/web"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="images")

# SEO-friendly image routes
@app.get("/nba-standings/{conference}/{date}.png")
async def get_standings_image(conference: str, date: str):
    """
    Serve standings images with clean, SEO-friendly URLs.
    Example: /nba-standings/eastern-conference/2025-12-17.png
    """
    filename = f"nba-{conference}-cumulative-standings-{date}.png"
    filepath = Path("img/standings") / filename
    if filepath.exists():
        return FileResponse(
            filepath,
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=31536000, immutable"
            }
        )
    return {"error": "Image not found"}, 404

# Serve index.html at root for SEO
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("src/web/index.html", "r") as f:
        return f.read()

@app.get("/hello-world")
async def hello_world():
    return "hi"
