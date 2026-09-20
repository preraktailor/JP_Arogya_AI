from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from rag.rag_engine import search_documents
from utils.ai_model import ask_ai


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# ----------------------------
# RAG PAGE
# ----------------------------
@router.get("/rag", response_class=HTMLResponse)
async def rag_page(request: Request):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="rag.html",
        context={
            "request": request,
            "user": request.session["user"]
        }
    )


# ----------------------------
# RAG SEARCH
# ----------------------------
@router.post("/rag", response_class=HTMLResponse)
async def rag_search(
    request: Request,
    question: str = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    context = search_documents(question)

    if context.strip():

        prompt = f"""
You are JP Arogya AI.

Use the medical context below to answer the user's question.

Medical Context:
{context}

Question:
{question}

Rules:
1. Explain in simple English.
2. Do not diagnose with certainty.
3. If information is not available in the context, clearly say so.
4. Recommend consulting a qualified doctor when appropriate.
5. Keep the answer concise.

This information is for educational purposes only and is not a substitute for professional medical advice.
"""

        answer = ask_ai(prompt)

    else:

        answer = ask_ai(question)

    return templates.TemplateResponse(
        request=request,
        name="rag.html",
        context={
            "request": request,
            "user": request.session["user"],
            "question": question,
            "answer": answer
        }
    )