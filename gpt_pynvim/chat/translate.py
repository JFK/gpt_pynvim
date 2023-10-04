from .completion import ChatCompletion
from ..common.errors import TranslateError
from ..common.config import LANGUAGE, TRANSLATE_USER_MESSAGE


class Translate(ChatCompletion):

    def __init__(self):
        super().__init__()

    def messages(self, user_message: str) -> list[dict[str, str]]:
        messages = []
        if TRANSLATE_USER_MESSAGE and LANGUAGE != "English":
            system = f"""Translate the following from {LANGUAGE} to English:"""
            user = f"""{user_message}"""
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        return messages

    def start(self, user_message: str) -> str:
        if not user_message:
            raise TranslateError("User message is empty")

        if TRANSLATE_USER_MESSAGE:
            try:
                messages = self.messages(user_message)
                if messages:
                    content = self.get_response_content(messages)
                    return content if content else user_message
            except Exception as e:
                raise TranslateError("An error occurred:", e)
        return user_message
