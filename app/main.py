from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api import router as api_router
from app.crowdsec_api import list_decisions

app = FastAPI(title="CrowdSec Web UI")

# Include API
app.include_router(api_router, prefix="/api")

# Templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    decisions = await list_decisions()
    return templates.TemplateResponse(
        request, "index.html", {"decisions": decisions}
    )
