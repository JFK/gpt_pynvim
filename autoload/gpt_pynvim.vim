if !has("python3")
  echo "Vim must be compiled with +python3 to run this plugin."
  echo "See :help python3-compile or"
  echo "Install neovim for Debian/Ubuntu:"
  echo "sudo add-apt-repository ppa:neovim-ppa/unstable"
  echo "sudo apt-get update"
  echo "sudo apt install neovim"
  finish
endif
if exists('g:gpt_pynvim_loaded')
  finish
endif

scriptencoding utf-8

function! s:CheckPythonDependencies()
  python3 << EOF
import pkg_resources
def check_dependencies():
    required_packages = {'pynvim': '0.4.3', 'openai': '0.28.0'}
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    missing_packages = {
        pkg: version for pkg, version in required_packages.items()
        if pkg not in installed_packages or installed_packages[pkg] < version
    }
    if missing_packages:
        print(f"Missing Python packages: {missing_packages}. Please install them.")
        vim.command("finish")
check_dependencies()
EOF
endfunction
autocmd VimEnter * :call s:CheckPythonDependencies()


let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
python3 << EOF
import sys
from os.path import normpath, join
plugin_root_dir = vim.eval('s:plugin_root_dir')
plugin_path = normpath(join(plugin_root_dir, '../'))
sys.path.insert(0, plugin_path)
from gpt_pynvim.common.config import (
    GPT_NVIM_CHAT_WINDOW,
    GPT_NVIM_CHAT_HISTORY_WINDOW,
    GPT_NVIM_CHAT_PROMPT_LOG_WINDOW,
    GPT_NVIM_CHAT_SUMMARIZE_URLS_WINDOW,
)
from gpt_pynvim import (
    vim_code_review,
    vim_chat,
    vim_chat_translate_to,
    vim_chat_selected_lines,
    vim_check_history,
    vim_clear_history,
    vim_summarize_urls,
    vim_check_prompt_log,
    vim_clear_prompt_log,
    print_config,
)
print_config()
EOF

function! g:gpt_pynvim#GptNvimCodeReview()
  python3 << EOF
vim_code_review(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction
vnoremap <buffer> . :<C-u>call g:gpt_pynvim#GptNvimCodeReview()<CR>


function! g:gpt_pynvim#GptNvimChat()
  python3 << EOF
vim_chat(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction
nnoremap <C-Enter> :call g:gpt_pynvim#GptNvimChat()<CR>


function! g:gpt_pynvim#GptNvimChatTranlateToEnglish()
  python3 << EOF
vim_chat_translate_to(GPT_NVIM_CHAT_WINDOW, "English")
EOF
endfunction
vnoremap <buffer> <C-e> :<C-u>call g:gpt_pynvim#GptNvimChatTranlateToEnglish()


function! g:gpt_pynvim#GptNvimChatTranlateTo()
  python3 << EOF
vim_chat_translate_to(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction
vnoremap <buffer> <C-t> :<C-u>call g:gpt_pynvim#GptNvimChatTranlateTo()


function! g:gpt_pynvim#GptNvimChatInsertSelectedLines()
  python3 << EOF
vim_chat_selected_lines(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction
vnoremap <buffer> <C-Enter> :<C-u>call g:gpt_pynvim#GptNvimChatInsertSelectedLines()


function! g:gpt_pynvim#GptNvimChatHistory()
  python3 << EOF
vim_check_history(GPT_NVIM_CHAT_HISTORY_WINDOW)
EOF
endfunction
command! GptNvimChatHistory :call g:gpt_pynvim#GptNvimChatHistory()


function! g:gpt_pynvim#GptNvimChatClearHistory()
  python3 << EOF
vim_clear_history(GPT_NVIM_CHAT_HISTORY_WINDOW)
EOF
endfunction
command! GptNvimChatClearHistory :call g:gpt_pynvim#GptNvimChatClearHistory()


function! g:gpt_pynvim#GptNvimChatPromptLog()
  python3 << EOF
vim_check_prompt_log(GPT_NVIM_CHAT_PROMPT_LOG_WINDOW)
EOF
endfunction
command! GptNvimChatPromptLog :call g:gpt_pynvim#GptNvimChatPromptLog()


function! g:gpt_pynvim#GptNvimChatClearPromptLog()
  python3 << EOF
vim_clear_prompt_log(GPT_NVIM_CHAT_PROMPT_LOG_WINDOW)
EOF
endfunction
command! GptNvimChatClearPromptLog :call g:gpt_pynvim#GptNvimChatClearPromptLog()


function! g:gpt_pynvim#GptNvimSummarizeUrls()
  python3 << EOF
vim_summarize_urls(GPT_NVIM_CHAT_SUMMARIZE_URLS_WINDOW)
EOF
endfunction
command! GptNvimSummarizeUrls :call g:gpt_pynvim#GptNvimSummarizeUrls()


function! g:gpt_pynvim#GptNvimSummarizeUrlsSend()
  python3 << EOF
vim_summarize_urls(GPT_NVIM_CHAT_SUMMARIZE_URLS_WINDOW)
EOF
endfunction
command! GptNvimSummarizeUrlsSend :call g:gpt_pynvim#GptNvimSummarizeUrlsSend()


function! g:gpt_pynvim#GptNvimUpdate()
  let l:parent_dir = fnamemodify(s:plugin_root_dir, ':h')
  let l:update_command = "cd " . l:parent_dir . "; git pull"
  call system(l:update_command)
  echo "gpt_nvim has been updated."
endfunction
command! GptNvimUpdate :call g:gpt_pynvim#GptNvimUpdate()


echo "\n[Usages]"
echo " `.` (dot) in visual mode to ask for a code review."
echo " `Ctrl+<Enter>` is equivalent to `:GptNvimChat` and `:GptNvimChatSend`."
echo " `:GptNvimChat` to open the buffer for questions."
echo " `:GptNvimChatSend` to send the question to GPT."
echo " `:GptNvimChatHistory` to check history of questions and answers."
echo " `:GptNvimChatClearHistory` to clear history of questions and answers."
echo " `:GptNvimChatPromptLog` to check prompt log."
echo " `:GptNvimChatClearPromptLog` to clear prompt log."
echo " `:GptNvimUpdate` to update the plugin."
echo " `:GptNvimSummarizeUrls` to summarize urls."
echo " `:GptNvimSummarizeUrlsSend` to summarize urls."
echo "\n"

let g:gpt_pynvim_loaded = 1
