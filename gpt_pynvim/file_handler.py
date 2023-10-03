import os
import json
import datetime
from .env import (
    CONTEXT_FILE_PATH,
    PROMPT_FILE_PATH
)


def save_context_to_file(context: dict):
    with open(CONTEXT_FILE_PATH, "w") as f:
        json.dump(context, f)


def load_context_from_file() -> dict[str, list]:
    with open(CONTEXT_FILE_PATH, "r") as f:
        return json.load(f)


def clear_context_file():
    with open(CONTEXT_FILE_PATH, "w") as f:
        json.dump({"context": []}, f)


def save_prompt_to_file(system_message: str = "", user_message: str = "",
                        assistant_reply: str = ""):
    with open(PROMPT_FILE_PATH, "a") as log_file:
        log_file.write(f"=={datetime.datetime.now()}]==\n")
        if system_message:
            log_file.write(f"[System]\n{system_message}\n")
        if user_message:
            log_file.write(f"[User]\n{user_message}\n")
        if assistant_reply:
            log_file.write(f"[Assistant]\n{assistant_reply}\n")


def load_prompt_from_file():
    with open(PROMPT_FILE_PATH, "r") as f:
        return f.read()


def clear_prompt_file():
    with open(PROMPT_FILE_PATH, "w") as f:
        f.write("")


if not os.path.exists(CONTEXT_FILE_PATH):
    try:
        save_context_to_file({"context": []})
    except Exception as e:
        print("Error: Can't create context file:", e)
        print(f"CONTEXT_FILE_PATH: {CONTEXT_FILE_PATH}")
        print("Please check if you have write permission to the plugin directory")
        exit(1)


if not os.path.exists(PROMPT_FILE_PATH):
    try:
        save_prompt_to_file("")
    except Exception as e:
        print("Error: Can't create prompt log file:", e)
        print(f"PROMPT_FILE_PATH: {PROMPT_FILE_PATH}")
        print("Please check if you have write permission to the plugin directory")
        exit(1)
