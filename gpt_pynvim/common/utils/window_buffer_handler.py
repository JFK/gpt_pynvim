import os
import vim

from ..config import (
    OPEN_WINDOW_DIRECTION,
    OPEN_WINDOW_SIZE,
)


def get_selected_lines() -> str:
    contents = []
    start_row, start_col = vim.eval('getpos("\'<")[1:2]')
    end_row, end_col = vim.eval('getpos("\'>")[1:2]')
    for row in range(int(start_row), int(end_row) + 1):
        line = vim.eval(f"getline({row})")
        # contents.append(line[int(start_col) - 1: int(end_col) - 1])
        contents.append(line)
    return "\n".join(contents)


def check_window_name(window_name: str) -> bool:
    for window in vim.windows:
        if os.path.basename(window.buffer.name) == window_name:
            return True
    vim.command(f"echo 'Error: {window_name} is not open.'")
    return False


def close_window(window_name: str):
    for window in vim.windows:
        if os.path.basename(window.buffer.name) == window_name:
            vim.api.win_close(window.handle, True)
            break


def open_window(window_name: str):
    close_window(window_name)
    vim.command(f"{OPEN_WINDOW_DIRECTION} {window_name}")
    set_common_vim_buffer_options()
    vim.command("startinsert")


def set_common_vim_buffer_options():
    # delete all text
    vim.command("normal! ggVGd")

    # set buffer options (non-file buffer)
    vim.command("setlocal buftype=nofile")

    # set window options (move to bottom, resize)
    if OPEN_WINDOW_DIRECTION == "vnew":
        vim.command("wincmd R")
        if OPEN_WINDOW_SIZE:
            vim.command(f"vertical resize {OPEN_WINDOW_SIZE}")
    else:
        vim.command("wincmd J")
        if OPEN_WINDOW_SIZE:
            vim.command(f"resize {OPEN_WINDOW_SIZE}")


def unsafe_update_window_buffer(window_name: str, buffer_content: str, mode: str = "a"):
    if not buffer_content:
        return

    for window in vim.windows:
        if os.path.basename(window.buffer.name) == window_name:
            vim.current.window = window
            break
    else:
        vim.command(f"{OPEN_WINDOW_DIRECTION} {window_name}")
        set_common_vim_buffer_options()

    messages = buffer_content.split("\n")
    if mode == "w":
        vim.current.buffer[:] = [line for line in messages if line]
        vim.command("normal gg")
    elif mode == "a":
        vim.current.buffer.append([line for line in messages if line])
        vim.command("normal G")


def update_window_buffer(window_name: str, buffer_content: str, mode: str = "a"):
    vim.async_call(unsafe_update_window_buffer, window_name, buffer_content, mode)
