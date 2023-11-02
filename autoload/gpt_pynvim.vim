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

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:parent_dir = fnamemodify(s:plugin_root_dir, ':h')

function! s:CheckPythonDependencies()
  python3 << EOF
try:
    from importlib.metadata import version, distributions # Python 3.8+
except ImportError:
    from importlib_metadata import version, distributions

def check_dependencies():
    required_packages = {'pynvim': '0.4.3', 'openai': '0.28.0', 'requests': '2.25.1', 'tiktoken': '0.5.1', 'markdownify': '0.11.6', 'bs4': '0.0.1'}
    
    installed_packages = {}
    for dist in distributions():
        installed_packages[dist.metadata['Name']] = dist.version

    missing_packages = {
        pkg: version for pkg, version in required_packages.items()
        if pkg not in installed_packages or installed_packages[pkg] < version
    }
    if missing_packages:
        parent_dir = vim.eval('s:parent_dir')
        print((
        f"Missing Python packages: {missing_packages}. Enter to install them.\n" +
        f"Installing Python dependencies from {parent_dir}/requirements.txt"
        ))
        cmd = f"pip3 install -r {parent_dir}/requirements.txt"
        vim.eval(f"system('{cmd}')")
check_dependencies()
EOF
endfunction
autocmd VimEnter * :call s:CheckPythonDependencies()

autocmd VimEnter,BufWinEnter * call s:InitGptPynvim()
function! s:InitGptPynvim()
  vnoremap <buffer> . :<C-u>call g:gpt_pynvim#GptNvimCodeReview()<CR>
  vnoremap <buffer> <C-Enter> :<C-u>call g:gpt_pynvim#GptNvimChatInsertSelectedLines()<CR>
  vnoremap <buffer> <C-t> :<C-u>call g:gpt_pynvim#GptNvimChatTranlateTo()<CR>
  vnoremap <buffer> <C-Enter> :<C-u>call g:gpt_pynvim#GptNvimChatInsertSelectedLines()<CR>
  nnoremap <C-Enter> :<C-u>call g:gpt_pynvim#GptNvimChat()<CR>
  nnoremap <C-t> :<C-u>call g:gpt_pynvim#GptNvimShowTemplateList()<CR>
endfunction


python3 << EOF
import vim
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
    vim_set_prompt_template,
    print_config,
)
print_config()
EOF


function! g:gpt_pynvim#GptNvimCodeReview()
  python3 << EOF
vim_code_review(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction


function! g:gpt_pynvim#GptNvimChat()
  python3 << EOF
vim_chat(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction


function! g:gpt_pynvim#GptNvimChatTranlateTo()
  python3 << EOF
vim_chat_translate_to(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction


function! g:gpt_pynvim#GptNvimChatInsertSelectedLines()
  python3 << EOF
vim_chat_selected_lines(GPT_NVIM_CHAT_WINDOW)
EOF
endfunction


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
  let l:update_command = "cd " . s:parent_dir . "; git pull"
  call system(l:update_command)
  echo "gpt_nvim has been updated."
endfunction
command! GptNvimUpdate :call g:gpt_pynvim#GptNvimUpdate()


let g:prompt_template_yaml_file =s:plugin_root_dir . '/prompt_template.yaml'
let g:own_prompt_template_yaml_file =s:parent_dir . '/prompt_template.yaml'

python3 << EOF
import yaml
import os
prompt_template_yaml_file = vim.vars['prompt_template_yaml_file']
own_prompt_template_yaml_file = vim.vars['own_prompt_template_yaml_file']
if os.path.isfile(own_prompt_template_yaml_file) and os.access(own_prompt_template_yaml_file, os.R_OK):
  prompt_template_yaml_file = own_prompt_template_yaml_file
with open(prompt_template_yaml_file, 'r') as f:
  data = yaml.safe_load(f)
vim.command('let s:prompt_template = ' + repr(data))
EOF
function! g:gpt_pynvim#GptNvimShowTemplateList()
  let template_list = []
  for i in range(len(s:prompt_template))
    let dict = s:prompt_template[i]
    let title = dict['title']
    call add(template_list, printf('%d: %s', i + 1, title))
  endfor
  let selected_index = inputlist(template_list)
  if empty(selected_index) || selected_index < 1 || selected_index > len(s:prompt_template)
      echo "\nInvalid selection!"
    return
  endif
  let selected_title = s:prompt_template[selected_index - 1]['title']
  let selected_content = s:prompt_template[selected_index - 1]['content']
  call GptNvimSelectTemplate(selected_title, selected_content)
endfunction
function! GptNvimSelectTemplate(selected_title, selected_content)
  echo "\nselected_template: " . a:selected_title
python3 << EOF
selected_content = vim.eval('a:selected_content')
selected_content = selected_content.replace('\\n', '\n')
vim_set_prompt_template(GPT_NVIM_CHAT_WINDOW, selected_content)
EOF
endfunction
command! GptNvimShowTemplates :call g:gpt_pynvim#GptNvimShowTemplateList()


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
