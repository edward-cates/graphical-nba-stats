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

@app.get("/nba-standings/eastern-conference/2026-03-24.png")
async def standings_east_2026_03_24():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-03-24.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-03-17.png")
async def standings_east_2026_03_17():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-03-17.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-03-10.png")
async def standings_east_2026_03_10():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-03-10.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-03-03.png")
async def standings_east_2026_03_03():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-03-03.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-02-26.png")
async def standings_east_2026_02_26():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-02-26.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-02-18.png")
async def standings_east_2026_02_18():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-02-18.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-02-11.png")
async def standings_east_2026_02_11():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-02-11.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-02-04.png")
async def standings_east_2026_02_04():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-02-04.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-01-28.png")
async def standings_east_2026_01_28():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-01-28.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-01-21.png")
async def standings_east_2026_01_21():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-01-21.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-01-14.png")
async def standings_east_2026_01_14():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-01-14.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2026-01-07.png")
async def standings_east_2026_01_07():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-01-07.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2025-12-31.png")
async def standings_east_2025_12_31():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2025-12-31.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/eastern-conference/2025-12-24.png")
async def standings_east_2025_12_24():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2025-12-24.png",
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

@app.get("/nba-standings/western-conference/2026-03-24.png")
async def standings_west_2026_03_24():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-03-24.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-03-17.png")
async def standings_west_2026_03_17():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-03-17.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-03-10.png")
async def standings_west_2026_03_10():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-03-10.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-03-03.png")
async def standings_west_2026_03_03():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-03-03.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-02-26.png")
async def standings_west_2026_02_26():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-02-26.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-02-18.png")
async def standings_west_2026_02_18():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-02-18.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-02-11.png")
async def standings_west_2026_02_11():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-02-11.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-02-04.png")
async def standings_west_2026_02_04():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-02-04.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-01-28.png")
async def standings_west_2026_01_28():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-01-28.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-01-21.png")
async def standings_west_2026_01_21():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-01-21.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-01-14.png")
async def standings_west_2026_01_14():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-01-14.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2026-01-07.png")
async def standings_west_2026_01_07():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-01-07.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2025-12-31.png")
async def standings_west_2025_12_31():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2025-12-31.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-standings/western-conference/2025-12-24.png")
async def standings_west_2025_12_24():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2025-12-24.png",
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

@app.get("/nba-head-to-head/2026-03-24.png")
async def head_to_head_2026_03_24():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-03-24.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-03-17.png")
async def head_to_head_2026_03_17():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-03-17.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-03-10.png")
async def head_to_head_2026_03_10():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-03-10.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-03-03.png")
async def head_to_head_2026_03_03():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-03-03.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-02-26.png")
async def head_to_head_2026_02_26():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-02-26.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-02-18.png")
async def head_to_head_2026_02_18():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-02-18.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-02-11.png")
async def head_to_head_2026_02_11():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-02-11.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-02-04.png")
async def head_to_head_2026_02_04():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-02-04.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-01-28.png")
async def head_to_head_2026_01_28():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-01-28.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-01-21.png")
async def head_to_head_2026_01_21():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-01-21.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-01-14.png")
async def head_to_head_2026_01_14():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-01-14.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2026-01-07.png")
async def head_to_head_2026_01_07():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-01-07.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2025-12-31.png")
async def head_to_head_2025_12_31():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2025-12-31.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-head-to-head/2025-12-24.png")
async def head_to_head_2025_12_24():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2025-12-24.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


# =============================================================================
# EAST VS WEST
# =============================================================================

@app.get("/nba-east-vs-west/2026-03-24.png")
async def east_vs_west_2026_03_24():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-03-24.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-03-17.png")
async def east_vs_west_2026_03_17():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-03-17.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-03-10.png")
async def east_vs_west_2026_03_10():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-03-10.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-03-03.png")
async def east_vs_west_2026_03_03():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-03-03.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-02-26.png")
async def east_vs_west_2026_02_26():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-02-26.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-02-18.png")
async def east_vs_west_2026_02_18():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-02-18.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-02-11.png")
async def east_vs_west_2026_02_11():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-02-11.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-02-04.png")
async def east_vs_west_2026_02_04():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-02-04.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-01-28.png")
async def east_vs_west_2026_01_28():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-01-28.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-01-21.png")
async def east_vs_west_2026_01_21():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-01-21.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-01-14.png")
async def east_vs_west_2026_01_14():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-01-14.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2026-01-07.png")
async def east_vs_west_2026_01_07():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-01-07.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2025-12-31.png")
async def east_vs_west_2025_12_31():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2025-12-31.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


@app.get("/nba-east-vs-west/2025-12-24.png")
async def east_vs_west_2025_12_24():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2025-12-24.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )


# =============================================================================
# LATEST (stable URLs for SEO - serve image directly, no redirect)
# =============================================================================

@app.get("/nba-standings/eastern-conference/latest.png")
async def standings_east_latest():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-2026-03-24.png",
        media_type="image/png",
    )


@app.get("/nba-standings/western-conference/latest.png")
async def standings_west_latest():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-2026-03-24.png",
        media_type="image/png",
    )


@app.get("/nba-head-to-head/latest.png")
async def head_to_head_latest():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-2026-03-24.png",
        media_type="image/png",
    )


@app.get("/nba-east-vs-west/latest.png")
async def east_vs_west_latest():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-2026-03-24.png",
        media_type="image/png",
    )


# =============================================================================
# PAGE ROUTES
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("src/web/index.html", "r") as f:
        return f.read()


@app.get("/nba-standings/", response_class=HTMLResponse)
async def nba_standings():
    with open("src/web/nba-standings.html", "r") as f:
        return f.read()


@app.get("/nba-head-to-head/", response_class=HTMLResponse)
async def nba_head_to_head():
    with open("src/web/nba-head-to-head.html", "r") as f:
        return f.read()


@app.get("/nba-east-vs-west/", response_class=HTMLResponse)
async def nba_east_vs_west():
    with open("src/web/nba-east-vs-west.html", "r") as f:
        return f.read()


@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse("src/web/sitemap.xml", media_type="application/xml")


@app.get("/robots.txt")
async def robots():
    return FileResponse("src/web/robots.txt", media_type="text/plain")


@app.get("/hello-world")
async def hello_world():
    return "hi"
