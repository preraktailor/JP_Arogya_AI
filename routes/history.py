from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database.db import get_chat_history, get_reports

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/history", response_class=HTMLResponse)
async def history(request: Request):

    if "user" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    email = request.session["user"]["email"]

    chats = get_chat_history(email)
    reports = get_reports(email)

    print("Session Email:", email)
    print("Chats:", chats)
    print("Reports:", reports)

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "user": request.session["user"],
            "chats": chats,
            "reports": reports
        }
    )