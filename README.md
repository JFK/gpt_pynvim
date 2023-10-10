# GPT-Pynvim

## Introduction

This plugin is a Neovim plugin that uses OpenAI's GPT model to generate code review and code-related question answers. It allows you to easily perform code reviews using Neovim and have conversations via the OpenAI API through Vim.

For example, you can select code in a file opened in Vim, press Enter, and a chat buffer window will open, displaying the selected code and allowing you to easily ask questions about it.

Additionally, you can select code and press dot to request a code review for the selected code from OpenAI.

Another feature is the ability to summarize the content of a URL by running `GptNvimSummarizeUrls` and inputting the URL.

If the response from OpenAI GPT does not fit within MAX_TOKENS, it will automatically retrieve the response again. The conversation context is stored only up to the number specified by GNVM_PRIOR_CONVERSAION_SIZE. If the size of chat completion messages exceeds the maximum tokens for each model, it will automatically select a higher-performance model (gpt-3.5-turbo-16k).

When you have a rectangular selection, pressing CTR+t allows you to easily translate the selected text. Pressing CTR+e translates it into English. CTR+T translates it into the language specified by LANGUAGE.


## The benefits of using GPT-Pynvim

1. Easy to code review
2. Easy to ask questions about code
3. Easy to summarize the content of a URL
4. Easy to translate text


## Requirements

- Vim with Python 3 support
- Python 3.10+
- Python packages: `pynvim>=0.4.3`, `openai>=0.28.0`
- Debain/Ubuntu package: `neovim>=0.9.0`

### Installing Neovim

See: https://github.com/neovim/neovim/wiki/Installing-Neovim


## Installation

1. Install required Debian/Ubutnu package:

```bash
sudo add-apt-repository ppa:neovim-ppa/stable
sudo apt-get update
sudo apt install neovim
```

2. Install the plugin using git clone:

```bash
cd ~/.config/nvim/plugin/
git clone https://github.com/jfk/gpt_pynvim.git
```

## Configuration

To use this plugin, you must set the OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```
### Optional configurations:
  
| Parameter                      | Description                      | Default Value      |
|--------------------------------|----------------------------------|--------------------|
| GNVM_OPENAI_MAX_TOKENS              | Maximum number of output tokens for OpenAI API | 1000        |
| GNVM_OPENAI_TEMPERATURE             | Temperature for OpenAI API       | 0.0                |
| GNVM_OPENAI_LANGUAGE                | Output Language                  | English           |
| GNVM_PRIOR_CONVERSAION_SIZE          | Number of coversation to remember  | 6                  |
| GNVM_CONTEXT_HISTORY_SIZE           | Number of history saving to context.json | 100        |
| GNVM_GPT_OPEN_VIM_WINDOW_DIRECTION  | Open window direction (This is only for GptNvimCodeReview and GptNvimCodeChat) | vnew |
| GNVM_GPT_OPEN_VIM_WINDOW_SIZE       | Open window size                 | None               |
| GNVM_TRANSLATE_USER_MESSAGE         | Translate user messages to English | 1         |
| GNVM_MODEL_AUTO_SELECT         | Select gpt-3.5-turbo-16k model based on input token length  | 1 |


## Usage

| Command                   | Description                                                |
|---------------------------|------------------------------------------------------------|
| `.` (in visual mode)      | Ask for a code review.                                     |
| `Ctrl+Enter`                | Open CptNvimChat and GptNvimChatSend.               |
| `Visual mode + Ctrl+t`   | While Visual mode, translate selected text.               |
| `Ctrl+t`               | Show selections of prompt templates.   |
| `:GptNvimChatHistory`  | Check history of questions and answers.                    |
| `:GptNvimChatClearHistory` | Clear history of questions and answers.                 |
| `:GptNvimChatPromptLog`| Check prompt log.                                          |
| `:GptNvimChatClearPromptLog` | Clear prompt log.                                   |
| `:GptNvimUpdate` | Update gpt-vim-code-reviewer plugin from Github.             |
| `:GptNvimSummarizeUrls` | Open the buffer for sumarize urls content.             |
| `:GptNvimSummarizeUrlsSend` | Summarize urls content. |


## Own prompt templates
To set up your own prompt templates, you can create a `prompt_templates.yaml` file in the `~/.config/nvim/plugin/gpt_pynvim` directory. By customizing this file, you can personalize and configure your preferred prompt templates. It's important to note that when you add your own prompt templates, the default ones will be disabled.

You just can copy `prompt_templates.yaml` from `~/.config/nvim/plugin/gpt_pynvim/autoload/prompt_templates.yaml` to `~/.config/nvim/plugin/gpt_pynvim` and edit it.

```bash
cp ~/.config/nvim/plugin/gpt_pynvim/autoload/prompt_templates.yaml ~/.config/nvim/plugin/gpt_pynvim
nvim ~/.config/nvim/plugin/gpt_pynvim/prompt_templates.yaml
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
