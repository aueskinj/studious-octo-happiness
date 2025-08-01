import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

app = FastAPI()

# Allow CORS from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

chat = ChatOllama(
    model="tinyllama",
    base_url="http://localhost:11434"
)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_with_model(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message", "").strip()

        if not user_message:
            raise HTTPException(status_code=400, detail="Message field is required.")

        result = chat.invoke([HumanMessage(content=user_message)])
        reply = getattr(result, 'content', str(result))

        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/test")
def test_connection():
    try:
        result = chat.invoke([HumanMessage(content="Hello, can you hear me?")])
        return {
            "status": "success",
            "result_type": str(type(result)),
            "has_content": hasattr(result, "content"),
            "content": getattr(result, "content", str(result))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test connection failed: {str(e)}")
