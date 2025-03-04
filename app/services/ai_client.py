from vertexai.language_models import CodeGenerationModel, CodeChatModel
from vertexai.preview.generative_models import GenerativeModel


class GeckoClient:
    def __init__(self):
        self.model = CodeGenerationModel.from_pretrained("code-gecko@latest")

    async def prompt(self, prefix, suffix):
        parameters = {"candidate_count": 1,
                      "max_output_tokens": 64, "temperature": 0.9}
        response = await self.model.predict_async(prefix, suffix=suffix, **parameters)
        return response


class BisonClient:
    def __init__(self):
        self.model = CodeChatModel.from_pretrained("codechat-bison@001")

    async def prompt(self, prompt_message: str, history: list = []):
        parameters = {
            "temperature": 0.5,
            "max_output_tokens": 500,
        }
        
        chat = self.model.start_chat(
            context="You are Nava Assist, an AI assistant for developers.You can write, explain and generate code and answer any user queries.",
            message_history=history
        )
        response = await chat.send_message_async(prompt_message, **parameters)
        
        del chat
        return response


class GeminiClient:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat()

    async def prompt(self, promptMessage):
        response = await self.chat.send_message_async(promptMessage, stream=True)
        return response


gecko_client = GeckoClient()
bison_client = BisonClient()
gemini_client = GeminiClient()
