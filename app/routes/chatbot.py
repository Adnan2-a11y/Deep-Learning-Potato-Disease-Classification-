from fastapi import APIRouter
import app.routes.explain as explain

router = APIRouter()

@router.get("/chatbot")
def simple_chatbot(query: str):
    """
    Very simple chatbot:
    - Looks for disease name in query
    - Returns explanation if found
    - Else returns default message
    """
    for disease, explanation in explain.items():
        if disease.lower().replace("_", " ") in query.lower():
            return {"answer": explanation}

    return {"answer": "I am not sure about that. Can you ask about a specific plant disease?"}


