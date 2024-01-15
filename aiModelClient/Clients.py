import vertexai
from vertexai.language_models import CodeGenerationModel, TextGenerationModel
from google.oauth2 import service_account
import os

class GeckoClient:
    def __init__(self):
        vertexai.init()
        self.model = CodeGenerationModel.from_pretrained("code-gecko@latest")

    async def prompt(self, prefix, suffix):
        parameters = {
            "candidate_count": 1,
            "max_output_tokens": 64,
            "temperature": 0.9
        }
        response = await self.model.predict_async(prefix, suffix = suffix, **parameters)
        return response

class BisonClient:
    def __init__(self):
        vertexai.init()
        self.model = TextGenerationModel.from_pretrained("text-bison@002")

    async def prompt(self, promptMessage):
        parameters = {
            "temperature": 0.5,
            "max_output_tokens": 500,
            "top_p": 0.8,
            "top_k": 40,
        }
        response = await self.model.predict_async(promptMessage, **parameters)
        return response