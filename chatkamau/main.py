import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

app = FastAPI()

# Allow CORS from all origins (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the chat model
chat = ChatOllama(
    model="tinyllama",
    base_url="http://localhost:11434"
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "LangChain Ollama API is running."}

@app.post("/chat")
async def chat_with_model(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message", "").strip()

        if not user_message:
            raise HTTPException(status_code=400, detail="Message field is required.")

        print(f"[User]: {user_message}")

        result = chat.invoke([HumanMessage(content=user_message)])

        # Extract and return the response
        reply = getattr(result, 'content', str(result))
        print(f"[TinyLLaMA]: {reply}")

        return {"response": reply}

    except Exception as e:
        print(f"Error during chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/test")
def test_connection():
    """
    Test endpoint to check if Ollama is working properly
    """
    try:
        test_prompt = "Hello, can you hear me?"
        result = chat.invoke([HumanMessage(content=test_prompt)])
        return {
            "status": "success",
            "result_type": str(type(result)),
            "has_content": hasattr(result, "content"),
            "content": getattr(result, "content", str(result))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test connection failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)