from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database.db import save_chat
from utils.ai_model import ask_ai

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):

    if "user" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "request": request,
            "user": request.session["user"]
        }
    )


@router.post("/chat", response_class=HTMLResponse)
async def chat(
    request: Request,
    question: str = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    # Get AI Response
    answer = ask_ai(question)

    # Save Chat
    save_chat(
        request.session["user"]["email"],
        question,
        answer
    )

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "request": request,
            "user": request.session["user"],
            "question": question,
            "answer": answer
        }
    )