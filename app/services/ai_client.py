from vertexai.language_models import CodeGenerationModel, CodeChatModel
from vertexai.preview.generative_models import GenerativeModel
import vertexai

class GeckoClient:
    def __init__(self):
        self.model = CodeGenerationModel.from_pretrained("code-gecko@latest")

    async def prompt(self, prefix, suffix):
        parameters = {"candidate_count": 1, "max_output_tokens": 64, "temperature": 0.9}
        response = await self.model.predict_async(prefix, suffix=suffix, **parameters)
        return response


class BisonClient:
    def __init__(self):
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
        self.model = GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat()

    async def prompt(self, promptMessage):
        response = await self.chat.send_message_async(promptMessage, stream=True)
        return response


gecko_client: GeckoClient | None = None
gemini_client: GeminiClient | None = None
bison_client: BisonClient | None = None

def initialize_clients():
    global gecko_client, gemini_client, bison_client
    vertexai.init()
    
    gecko_client = GeckoClient()
    gemini_client = GeminiClient()
    bison_client = BisonClient()