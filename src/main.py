import os
from pathlib import Path
import json

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

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

# Cache headers for immutable images
CACHE_HEADERS = {"Cache-Control": "public, max-age=31536000, immutable"}


# =============================================================================
# STANDINGS - Eastern Conference
# =============================================================================

@app.get("/nba-standings/eastern-conference/2025-12-20.png")
async def standings_east_2025_12_20():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2025-12-20.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2025-12-17.png")
async def standings_east_2025_12_17():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2025-12-17.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


# =============================================================================
# STANDINGS - Western Conference
# =============================================================================

@app.get("/nba-standings/western-conference/2025-12-20.png")
async def standings_west_2025_12_20():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2025-12-20.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2025-12-17.png")
async def standings_west_2025_12_17():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2025-12-17.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


# =============================================================================
# HEAD-TO-HEAD
# =============================================================================

@app.get("/nba-head-to-head/2025-12-20.png")
async def head_to_head_2025_12_20():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2025-12-20.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


# =============================================================================
# EAST VS WEST
# =============================================================================

@app.get("/nba-east-vs-west/2025-12-20.png")
async def east_vs_west_2025_12_20():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2025-12-20.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


# =============================================================================
# PAGE ROUTES
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("src/web/index.html", "r") as f:
        return f.read()


@app.get("/nba-standings", response_class=HTMLResponse)
async def nba_standings():
    with open("src/web/nba-standings.html", "r") as f:
        return f.read()


@app.get("/nba-head-to-head", response_class=HTMLResponse)
async def nba_head_to_head():
    with open("src/web/nba-head-to-head.html", "r") as f:
        return f.read()


@app.get("/nba-east-vs-west", response_class=HTMLResponse)
async def nba_east_vs_west():
    with open("src/web/nba-east-vs-west.html", "r") as f:
        return f.read()


@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse("src/web/sitemap.xml", media_type="application/xml")


@app.get("/hello-world")
async def hello_world():
    return "hi"
