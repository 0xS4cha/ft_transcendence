import requests
import json
from shared.database import db


class ChatBot:
	def __init__(self, model_name: str, system_prompt: str):
		self.model_name = model_name
		self.open_router_api_key = db.settings.OPENROUTER_API_KEY
		self.system_prompt = system_prompt


	def ask(self, message: str):
		response = requests.post(
			url="https://openrouter.ai/api/v1/chat/completions",
			headers={
				"Authorization": f"Bearer {self.open_router_api_key}",
				"Content-Type": "application/json",
			},
			data=json.dumps({
				"model": self.model_name,
				"messages": [
					{
						"role": "system",
						"content": self.system_prompt
					},
					{
						"role": "user",
						"content": message
					}
				],
				"reasoning": {"enabled": True}
			})
		)

		response = response.json()
		return response['choices'][0]['message']

