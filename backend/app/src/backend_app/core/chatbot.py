from ollama import AsyncClient


class ChatBot:
	def __init__(self, model_name: str, system_prompt: str):
		self.model_name = model_name
		self.client = AsyncClient(host="http://host.docker.internal:11434")
		self.system_prompt = system_prompt


	async def ask(self, message: str):
		response = await self.client.chat(
			model=self.model_name,
			messages=[
				{
					"role": "system",
					"content": self.system_prompt
				},
				{
					"role": "user",
					"content": message
				},
			],
		)
		return response["message"]["content"]


