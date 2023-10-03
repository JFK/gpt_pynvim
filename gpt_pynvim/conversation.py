from .chat_completion import ChatCompletion
from .code_review import code_review_messages
from .translate import Translate
from .errors import ConversationError
from .env import (
    LANGUAGE,
    MAX_TOKENS,
    PRIOR_CONVERSAION_SIZE,
    CONTEXT_HISTORY_SIZE,
)
from .file_handler import (
    load_context_from_file,
    save_context_to_file,
    save_prompt_to_file,
)
from .window_buffer_handler import update_window_buffer


class Conversation(ChatCompletion):

    def __init__(self):
        super().__init__()
        self._context_data = load_context_from_file()
        self._translate = Translate()
        self._prior_conversation = []
        self._code_review_flag = False

    def set_code_review_flag(self, flag: bool):
        self._code_review_flag = flag

    @property
    def context(self) -> list[dict[str, str]]:
        self._context_data = load_context_from_file()
        return self._context_data["context"]

    def conversation_messages(
        self, user_message: str, prior_conversation: list[dict[str, str]] = None
    ) -> list[dict[str, str]]:
        system = (
            "You are a programming specialist assisting a programmer. " +
            f"Respond in {LANGUAGE}, concisely, within {MAX_TOKENS} tokens. " +
            "If unsure, reply 'I don't know'. "
        )
        messages = [{"role": "system", "content": system}]
        if prior_conversation:
            for message in prior_conversation:
                messages.extend(message)
        messages.append({"role": "user", "content": user_message})
        return messages

    def get_prior_conversation(self) -> list[dict[str, str]]:
        return self.context[-PRIOR_CONVERSAION_SIZE:] if self.context else []

    def display_context(self, context: list[dict[str, str]] = None):
        if not context:
            context = self.context
        for user_and_assistant in context:
            q = ""
            a = ""
            for message in user_and_assistant:
                if message["role"] == "user":
                    q = message["content"]
                    update_window_buffer(self.window_name, f"\nQ:{q}\n")
                elif message["role"] == "assistant":
                    a = message["content"]
                    update_window_buffer(self.window_name, f"\nA:{a}\n")

    def save_context_to_file(self, user_message: str, content: str):
        conversation = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": content}
        ]
        self._context_data["context"].append(conversation)

        self._context_data["context"] = self._context_data["context"][
            -CONTEXT_HISTORY_SIZE:
        ]
        save_context_to_file(self._context_data)

    def save_prompt_to_file(self, conversation: list[dict[str, str]], content: str):
        user_messages = []
        for message in conversation:
            if message["role"] == "user":
                user_messages.append(message["content"])
            elif message["role"] == "system":
                system_message = message["content"]
        save_prompt_to_file(system_message, "\n".join(user_messages), content)

    def start(self, user_message: str) -> str:
        try:
            if not user_message:
                raise ConversationError("User message is empty.")
            self._prior_conversation = self.get_prior_conversation()
            messages = []
            if self._code_review_flag:
                messages = code_review_messages(user_message,
                                                self._prior_conversation)
            else:
                user_message = self._translate.start(user_message)
                messages = self.conversation_messages(user_message,
                                                      self._prior_conversation)
            content = self.get_response_content(messages)
            self.save_context_to_file(user_message, content)
            self.save_prompt_to_file(messages, content)
            return content
        except Exception as e:
            raise ConversationError("An error occurred:", e)
