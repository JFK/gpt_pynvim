import vim
import threading
from .common.config import (
    DEBUG,
    MAX_TOKENS,
    TEMPERATURE,
    LANGUAGE,
    PRIOR_CONVERSAION_SIZE,
    CONTEXT_HISTORY_SIZE,
    OPEN_WINDOW_DIRECTION,
    OPEN_WINDOW_SIZE,
    OPENAI_API_MODEL_NAME,
    ALLOWED_MODELS,
    CONTEXT_FILE_PATH,
    PROMPT_FILE_PATH,
)
from .common.utils.window_buffer_handler import (
    update_window_buffer,
    close_window,
    open_window,
    check_window_name,
    unsafe_update_window_buffer,
    set_common_vim_buffer_options,
    get_selected_lines,
)
from .common.utils.file_handler import (
    load_prompt_from_file,
    clear_context_file,
    clear_prompt_file,
)
from .common.errors import ChatCompletionError
from .chat.conversation import Conversation
from .chat.generate_summary import GenerateSummary


conversation = Conversation()
generate_summary = GenerateSummary()


def print_config():
    if DEBUG:
        print("[GPTNvim settings]")
        print(" MODEL:", OPENAI_API_MODEL_NAME)
        print(" AVAILABLE MODEL:", ", ".join(ALLOWED_MODELS))
        print(" LANGUAGE:", LANGUAGE)
        print(" MAX TOKEN:", MAX_TOKENS)
        print(" PRIOR CONVERSAION SIZE:", PRIOR_CONVERSAION_SIZE)
        print(" CONTEXT HISTORY SIZE:", CONTEXT_HISTORY_SIZE)
        print(" TEMPERATURE:", TEMPERATURE)
        print(" CONTEXT FILE PATH:", CONTEXT_FILE_PATH)
        print(" PROMPT FILE PATH:", PROMPT_FILE_PATH)
        print(" OPEN WINDOW DIRECTION:", OPEN_WINDOW_DIRECTION)
        if OPEN_WINDOW_SIZE:
            print(" Open window size", OPEN_WINDOW_SIZE)


def conversation_start(
    window_name: str, user_message: str, code_review_flag: bool = False
):
    conversation.set_window_name(window_name)
    if code_review_flag:
        conversation.set_code_review_flag(True)
    message = user_message
    mode = "w"
    loop_count = 0
    while True:
        try:
            content = conversation.start(message)
        except ChatCompletionError as e:
            vim.async_call(vim.command, f'echo "{e}"')
            break
        update_window_buffer(window_name, content, mode)
        if conversation.finish_reason == "stop":
            message = "Conversation finished."
            if code_review_flag:
                message = "Code review done and conversation history cleared."
                clear_context_file()
                conversation.set_code_review_flag(False)
            vim.async_call(vim.command, f'echo "{message}"')
            break
        else:
            vim.async_call(vim.command, "echo 'Conversation continuing.'")
            message = "Please continue from where it left off."
            mode = "a"
        loop_count += 1
        if loop_count > PRIOR_CONVERSAION_SIZE:
            message = f"Loop count exceeded {loop_count}.\nConversation stopped."
            vim.async_call(vim.command, f'echo "{message}"')
            break


def generate_summary_start(window_name: str, buffer_content: str):
    generate_summary.set_window_name(window_name)
    update_window_buffer(window_name, "Please wait. AI is thinking...", "w")
    try:
        content = generate_summary.start(window_name, buffer_content)
    except ChatCompletionError as e:
        vim.async_call(vim.command, f'echo "{e}"')
    update_window_buffer(window_name, content, "w")


def display_please_wait_message(window_name: str, buffer_content: str):
    message = (
        "Start sending the following message.\n"
        + "It takes a while to get the answer from GPT.\n"
        + "Please wait patiently. \n"
        + "Thank you for your patience.\n"
        + "\n"
        + "[Buffer content]\n"
        + f"\n{buffer_content}\n"
    )
    unsafe_update_window_buffer(window_name, message, "w")


def vim_clear_prompt_log(window_name: str):
    close_window(window_name)
    clear_prompt_file()
    vim.command('echo "Prompt log cleared."')


def vim_check_prompt_log(window_name: str):
    log_text = load_prompt_from_file()
    if log_text:
        close_window(window_name)
        vim.command(f"new {window_name}")
        set_common_vim_buffer_options()
        vim.command("wincmd J")
        vim.command("normal G")
        unsafe_update_window_buffer(window_name, log_text, "w")
    else:
        vim.command('echo "Prompt log is empty."')


def vim_clear_history(window_name: str):
    close_window(window_name)
    clear_context_file()
    vim.command('echo "History cleared."')


def vim_check_history(window_name: str):
    if conversation.context:
        close_window(window_name)
        vim.command(f"new {window_name}")
        set_common_vim_buffer_options()
        vim.command("wincmd J")
        vim.command("normal G")
        conversation.set_window_name(window_name)
        conversation.display_context()
    else:
        vim.command('echo "History not found."')


def vim_chat_translate_to(window_name: str, language: str = LANGUAGE):
    selected_lines = get_selected_lines()
    if not selected_lines:
        vim.command('echo "Error: Empty message."')
        return
    message = f"Translate to {language}.\n```\n{selected_lines}\n```"
    unsafe_update_window_buffer(window_name, message, "w")


def vim_chat_selected_lines(window_name: str):
    selected_lines = get_selected_lines()
    if not selected_lines:
        vim.command('echo "Error: Empty message."')
        return
    unsafe_update_window_buffer(window_name, f"```\n{selected_lines}\n```", "w")


def vim_chat(window_name: str):
    if not check_window_name(window_name):
        open_window(window_name)
        return
    buffer_content = "\n".join(vim.current.buffer)
    if not buffer_content:
        vim.command('echo "Error: Empty message."')
        return
    display_please_wait_message(window_name, buffer_content)
    thread = threading.Thread(
        target=conversation_start,
        args=(
            window_name,
            buffer_content,
        ),
    )
    thread.start()


def vim_summarize_urls(window_name: str):
    if not check_window_name(window_name):
        open_window(window_name)
        message = (
            "Please enter your message and press Ctrl + <Enter>. "
            + "And press `d` to delete this message."
        )
        update_window_buffer(window_name, message, "w")
        vim.command("normal V$")
        return
    buffer_content = "\n".join(vim.current.buffer)
    if not buffer_content:
        vim.command('echo "Error: Empty urls."')
        return
    display_please_wait_message(window_name, buffer_content)
    thread = threading.Thread(
        target=generate_summary_start,
        args=(
            window_name,
            buffer_content,
        ),
    )
    thread.start()


def vim_code_review(window_name: str):
    clear_context_file()
    message = "Code review started and conversation history cleared."
    vim.command(f'echo "{message}"')
    selected_code = get_selected_lines()
    display_please_wait_message(window_name, selected_code)
    thread = threading.Thread(
        target=conversation_start,
        args=(
            window_name,
            selected_code,
            True,
        ),
    )
    thread.start()


def vim_set_prompt_template(window_name: str, prompt_template):
    if not prompt_template:
        vim.command('echo "Error: Empty prompt template."')
        return
    unsafe_update_window_buffer(window_name, f"{prompt_template}", "w")
