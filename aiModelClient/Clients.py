import vertexai
from vertexai.language_models import CodeGenerationModel, CodeChatModel
from vertexai.preview.generative_models import GenerativeModel
import google.generativeai as genai
from google.oauth2 import service_account
import os

class Config:
    def __init__(self):
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
        self.location = os.environ.get('GOOGLE_CLOUD_LOCATION')
        file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        self.credentials = service_account.Credentials.from_service_account_file(file_path)

class GeckoClient:
    def __init__(self):
        self.config = Config()
        vertexai.init(project=self.config.project_id,
                      location=self.config.location, 
                      credentials=self.config.credentials)
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
        self.config = Config()
        vertexai.init(project=self.config.project_id,
                      location=self.config.location, 
                      credentials=self.config.credentials)
        self.model = CodeChatModel.from_pretrained("codechat-bison@001")
        self.chat = self.model.start_chat(
            context="You are Nava Assist, an AI assistant for developers.You can write, explain and generate code and answer any user queries."
        )
        
    async def prompt(self, promptMessage):
        parameters = {
            "temperature": 0.5,
            "max_output_tokens": 500,
        }
        response = await self.chat.send_message_async(promptMessage, **parameters)
        return response

class GeminiClient:
    def __init__(self):
        self.config = Config()
        vertexai.init(project=self.config.project_id,
                      location=self.config.location, 
                      credentials=self.config.credentials)
        self.model = GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat()
        
    async def prompt(self, promptMessage):
        response = await self.chat.send_message_async(promptMessage, stream=True)
        return response

class GeminiClientGenAi:
    def __init__(self):
        GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat()
        
    def prompt(self, promptMessage):
        response = self.chat.send_message(promptMessage, stream=True)
        return response