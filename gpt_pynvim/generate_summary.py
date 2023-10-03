from typing import Any
import json
import re

from bs4 import BeautifulSoup
from markdownify import markdownify as md
import requests

from .chat_completion import ChatCompletion
from .errors import GenerateSummaryError
from .env import LANGUAGE
from .window_buffer_handler import update_window_buffer


class GenerateSummary(ChatCompletion):

    def __init__(self, chunk_size: int = 1000):
        super().__init__()
        self._chunk_size = chunk_size

    def generate_summary_messages(
        self, title: str, chunk: str, prior_summary: str = ""
    ) -> list[dict[str, str]]:
        user_message = f"""
        Extract key information from the following text and summarize it.
        Title: {title}
        Body:
        ```
        {prior_summary}
        ---
        {chunk}
        ```
        Output language: {LANGUAGE} Summary length: less than 500 words but useful examples are more important than the length.
        """
        messsages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ]
        return messsages

    def remove_links_from_markdown(self, text: str) -> str:
        return text.replace("[", "").replace("]", "")

    def build_chunks_from_markdown(self, markdown: str) -> list[str]:
        content_markdown = md(markdown)
        markdown = self.remove_links_from_markdown(content_markdown)
        markdown = re.sub(r"\s+", " ", markdown)
        markdown = re.sub(r"\n+", "\n", markdown)
        return [
            markdown[i: i + self._chunk_size]
            for i in range(0, len(markdown), self._chunk_size)
        ]

    def request(self, url: str) -> tuple[str, str]:
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            text = resp.text
            soup = BeautifulSoup(text, "html.parser")
            title = soup.title.string
            return (title, soup.get_text())
        except requests.RequestException as error:
            raise GenerateSummaryError(
                f"An error occurred during your request: {error}"
            )
        except Exception as error:
            raise GenerateSummaryError(f"An error occurred: {error}")

    def get_functions(self) -> list[dict[str, Any]]:
        functions = [
            {
                "name": "find_urls",
                "description": "Find urls in text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "urls": {
                            "type": "array",
                            "description": "List of urls to summarize",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["urls"],
                },
            }
        ]
        return functions

    def find_urls(self, text: str) -> list[str]:
        functions = self.get_functions()
        messages = [{"role": "user", "content": text}]
        message = self.get_response_message(messages, functions)
        arguments = json.loads(message["function_call"]["arguments"])
        return arguments.get("urls", [])

    def convert_summary_to_text(self, summaries: list[dict[str, str]]) -> str:
        message = ""
        for summary in summaries:
            message += "\n\n===Summary===\n"
            message += f"[URL]\n{summary['url']}\n"
            message += f"[Summary]\n{summary['summary']}"
        return message

    def from_urls(self, urls: list[str]) -> list[dict[str, str]]:
        if not urls and not isinstance(urls, list):
            raise GenerateSummaryError("URLs are empty or not a list.")
        summary_and_url = []
        for url in urls:
            update_window_buffer(self.window_name, f"Target url: {url}")
            try:
                title, html_body_text = self.request(url)
                chunks = self.build_chunks_from_markdown(html_body_text)
                prior_summary = ""
                for chunk in chunks:
                    update_window_buffer(self.window_name, f"Chunk: {chunk}")
                    messages = self.generate_summary_messages(
                        title, chunk, prior_summary
                    )
                    prior_summary = self.get_response_content(messages)
                summary_and_url.append({"summary": prior_summary, "url": url})
            except Exception as e:
                raise GenerateSummaryError(f"An error occurred: {e}")
        return summary_and_url

    def start(self, text: str) -> str:
        urls = self.find_urls(text)
        summaries = self.from_urls(urls)
        return self.convert_summary_to_text(summaries)
