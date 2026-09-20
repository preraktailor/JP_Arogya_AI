from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database.db import create_database

# Routers
from routes.auth import router as auth_router
from routes.dashboard import router as dashboard_router
from routes.chatbot import router as chatbot_router
from routes.upload import router as upload_router
from routes.history import router as history_router
from routes.rag import router as rag_router


app = FastAPI(
    title="JP Arogya AI",
    description="AI Healthcare Assistant using OCR + AI",
    version="1.0"
)


# ----------------------------
# SESSION
# ----------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key="jp_arogya_ai_secret_key"
)


# ----------------------------
# STATIC FILES
# ----------------------------
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


templates = Jinja2Templates(
    directory="templates"
)


# ----------------------------
# DATABASE
# ----------------------------
create_database()


# ----------------------------
# HOME
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ----------------------------
# REGISTER ROUTERS
# ----------------------------
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(chatbot_router)
app.include_router(upload_router)
app.include_router(history_router)
app.include_router(rag_router)