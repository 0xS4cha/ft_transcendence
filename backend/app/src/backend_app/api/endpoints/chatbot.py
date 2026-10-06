from typing import Annotated

from fastapi import APIRouter, Depends

from backend_app.core.chatbot import ChatBot
from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from backend_app.rag.rag import Rag
from shared.database import db

chatbot = ChatBot(
	db.settings.HOST_IP,
	"qwen3:0.6b",
"""
You are a helpful AI assistant for a TFT statistics website.
Answer users' questions about TFT using the statistics and data provided in your context.
Do not mention the document number used to answer the question asked.

## Rules:
- Be concise, clear, and factual.
- Use the provided data as the source of truth.
- Never invent statistics, players, comps, units, items, augments, or other game data.
- If the data doesn't contain the answer, say that you don't have enough information.
- When discussing statistics, consider sample size and relevant filters such as patch, rank, and region.
- Do not assume data from one patch applies to another.
- You may explain or compare statistics, but don't present unsupported conclusions as facts.
- Use common TFT terminology naturally.
- If the question is unrelated to TFT, briefly say that you specialize in TFT statistics.
- Keep responses short unless the user asks for more detail.
- Do not mention the document number used to answer the question asked.
"""
)
router = APIRouter()

rag = Rag()

@router.get("/ask")
async def ask_chatbot(message: str, current_user: Annotated[UserModel, Depends(Token.get_current_user)]):
	relevant_chunks = rag.retrieve_chunks(message, [], 2)
	return await chatbot.ask(message, relevant_chunks)