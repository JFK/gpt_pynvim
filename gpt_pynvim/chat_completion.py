from os import environ
from typing import Any
import openai
import tiktoken
import vim

from .errors import ChatCompletionError
from .env import (
    OPENAI_API_MODEL_NAME,
    ALLOWED_MODELS,
    MODEL_NAME_FOR_LONG_MESSAGES,
    MAX_TOKENS_SIZE,
    MAX_TOKENS,
    TEMPERATURE,
    MODEL_AUTO_SELECT,
)


openai.api_key = environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("Error: OPENAI_API_KEY is not set")
    exit(1)


if OPENAI_API_MODEL_NAME not in ALLOWED_MODELS:
    print(
        (
            f"Error: Invalid model name: {OPENAI_API_MODEL_NAME},"
            f"allowed models: {ALLOWED_MODELS}"
        )
    )
    exit(1)


class ChatCompletion:

    def __init__(self):
        self._window_name = None
        self._finish_reason = None

    def set_window_name(self, value: str):
        self._window_name = value

    def reset_finish_reason(self):
        self._finish_reason = None

    @property
    def window_name(self) -> str:
        if not self._window_name:
            raise ChatCompletionError("Window name not set.")
        return self._window_name

    @property
    def finish_reason(self) -> str:
        return self._finish_reason

    def num_tokens_from_string(self, content: str) -> int:
        encoding = tiktoken.encoding_for_model(OPENAI_API_MODEL_NAME)
        num_tokens = len(encoding.encode(content))
        return num_tokens

    def calculate_token_count(self, messages: list[dict[str, str]]) -> int:
        return sum(self.num_tokens_from_string(c["content"]) for c in messages)

    def run_model_auto_select(self, messages: list[dict[str, str]]) -> str:
        if not messages:
            return OPENAI_API_MODEL_NAME
        conversation_token_count = self.calculate_token_count(messages)
        max_token_size = MAX_TOKENS_SIZE.get(OPENAI_API_MODEL_NAME, 2048)
        available_token_size = max_token_size - MAX_TOKENS
        if MODEL_AUTO_SELECT:
            if conversation_token_count > available_token_size:
                message = (
                    "!!!!WARNING!!!!\n" +
                    f"Messages token count: ({conversation_token_count})\n" +
                    f"Available token size: ({available_token_size}).\n" +
                    f"Selected model: {MODEL_NAME_FOR_LONG_MESSAGES}."
                )
                vim.async_call(vim.command, f"echo \"{message}\"")
                return MODEL_NAME_FOR_LONG_MESSAGES
        return OPENAI_API_MODEL_NAME

    def get_content(self, response: dict[str, Any]) -> str:
        content = ""
        try:
            content = response["choices"][0]["message"]["content"]
            self._finish_reason = response["choices"][0]["finish_reason"]
        except Exception as e:
            raise ChatCompletionError("Failed to parse response.", e)
        return content

    def get_message(self, response: dict[str, Any]) -> dict[str, Any]:
        message = {}
        try:
            message = response["choices"][0]["message"]
        except Exception as e:
            raise ChatCompletionError("Failed to parse response.", e)
        return message

    def get_response_content(self, messages: list[dict[str, str]]) -> str:
        if not messages:
            return ""
        response = self.create(messages)
        return self.get_content(response)

    def get_response_message(self, messages: list[dict[str, str]],
                             functions: dict[str, Any]) -> dict[str, Any]:
        if not messages:
            return {}
        options = {"functions": functions, "function_call": "auto"}
        response = self.create(messages, **options)
        return self.get_message(response)

    def create(self, messages: list[dict[str, str]], **kwargs):
        default_chat_options = {
            "model": OPENAI_API_MODEL_NAME,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        }
        model_name = self.run_model_auto_select(messages)
        options = {**default_chat_options, **kwargs}
        options["model"] = model_name
        if messages:
            options["messages"] = messages
        try:
            response = openai.ChatCompletion.create(**options)
            return response
        except Exception as e:
            raise ChatCompletionError(e)
