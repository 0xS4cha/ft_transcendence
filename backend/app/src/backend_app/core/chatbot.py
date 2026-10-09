import logging

from ollama import AsyncClient

logger = logging.getLogger(__name__)


class ChatBot:
	def __init__(self, host_ip: str, model_name: str, system_prompt: str):
		self.model_name = model_name
		self.client = AsyncClient(host=f"http://{host_ip}:11434", timeout=120)
		self.system_prompt = system_prompt


	async def ask(self, message: str, relevant_chunks: list[str]):
		try:
			context = "\n\n".join(
				f"[Document {len(relevant_chunks) - i}]\n{chunk}"
				for i, chunk in enumerate(relevant_chunks)
			)
			response = await self.client.chat(
				model=self.model_name,
				messages=[
					{
						"role": "system",
						"content": self.system_prompt
					},
					{
						"role": "user",
						"content": f"Context:\n{context}\n\nQuestion:\n{message}",
					}
				],
			)
			return response["message"]["content"]
		except Exception as e: #noqa: BLE001
			logger.warning(e)
			return "Could not access chatbot for the moment, try again later"


