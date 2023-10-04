import os

DEBUG = int(os.environ.get("GNVM_DEBUG", 0))

# Buffer window names
GPT_NVIM_CODE_REVIEW_WINDOW = "GptNvimCodeReviewWindow"
GPT_NVIM_CHAT_WINDOW = "GptNvimChatWindow"
GPT_NVIM_CHAT_HISTORY_WINDOW = "GptNvimChatHistoryWindow"
GPT_NVIM_CHAT_PROMPT_LOG_WINDOW = "GptNvimChatPromptLogWindow"
GPT_NVIM_CHAT_SUMMARIZE_URLS_WINDOW = "GptNvimChatSummarizeUrlsWindow"

# Global variables
MAX_TOKENS = int(os.environ.get("GNVM_OPENAI_MAX_TOKENS", 500))
TEMPERATURE = float(os.environ.get("GNVM_OPENAI_TEMPERATURE", 0.0))
LANGUAGE = os.environ.get("GNVM_OPENAI_LANGUAGE", "English")
PRIOR_CONVERSAION_SIZE = int(os.environ.get("GNVM_PRIOR_CONVERSAION_SIZE", 6))
CONTEXT_HISTORY_SIZE = int(os.environ.get("GNVM_CONTEXT_HISTORY_SIZE", 100))
OPEN_WINDOW_DIRECTION = os.environ.get("GNVM_GPT_OPEN_VIM_WINDOW_DIRECTION", "vnew")
OPEN_WINDOW_SIZE = os.environ.get("GNVM_GPT_OPEN_VIM_WINDOW_SIZE", None)
TRANSLATE_USER_MESSAGE = os.environ.get("GNVM_TRANSLATE_USER_MESSAGE", 0)
MODEL_AUTO_SELECT = os.environ.get("GNVM_MODEL_AUTO_SELECT", 1)
CONTEXT_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "context.json"
)
PROMPT_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompt.log"
)

OPENAI_API_MODEL_NAME = os.environ.get("OPENAI_API_MODEL_NAME", "gpt-3.5-turbo")
MAX_TOKENS_SIZE = {
    "gpt-3.5-turbo": 4097,
    "gpt-4": 2048,
    "gpt-3.5-turbo-16k": 16384,
}
MODEL_NAME_FOR_LONG_MESSAGES = "gpt-3.5-turbo-16k"
ALLOWED_MODELS = list(MAX_TOKENS_SIZE.keys())

