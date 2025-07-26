from fastapi import FastAPI
from uuid import uuid4
from database import db
from schemas import ChatRequest, ChatResponse
# from llm import ask_llm
from datetime import datetime, timezone
from llm import ask_llm_with_context

app = FastAPI()

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Step 1: Create conversation if not given
    now = datetime.now(timezone.utc)
    if request.conversation_id:
        conv_id = request.conversation_id
    else:
        conv_id = str(uuid4())
        await db["sessions"].insert_one({
            "_id": conv_id,
            "user_id": request.user_id,
            "created_at":now
        })

    # Step 2: Save user message
    await db["messages"].insert_one({
        "session_id": conv_id,
        "sender": "user",
        "message": request.message,
        "timestamp":now
    })

    # Step 3: Ask LLM
    ai_reply = await ask_llm_with_context(request.message)


    # Step 4: Save AI message
    

    await db["messages"].insert_one({
        "session_id": conv_id,
        "sender": "ai",
        "message": ai_reply,
        "timestamp":now
    })

    # Step 5: Return
    return ChatResponse(conversation_id=conv_id, response=ai_reply)
