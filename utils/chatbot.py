import os
import re
import time

from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI

from utils.prompts.chatbot_prompts import chat_prompt

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAiQuery:
    def __init__(self, model_type="gpt-4o-mini", llm="open_ai"):
        self.key = OPENAI_API_KEY
        self.model_type = model_type

        if llm == "open_ai":
            self.llm = ChatOpenAI(model=self.model_type, openai_api_key=self.key)
        elif llm == "ollama":
            self.llm = OllamaLLM(model=model_type)
        else:
            self.llm = ChatOpenAI(model=self.model_type, openai_api_key=self.key)

    def chat(self, query):
        print("Chatbot is thinking...")
        prompt = chat_prompt.replace("{question}", query)

        response = self.llm.invoke(prompt)

        try:
            think_content = None
            answer = response.content
        except:
            # Extract the content inside <think> tags
            think_match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
            think_content = think_match.group(1).strip()
            response = re.sub(
                r"<think>.*?</think>", "", response, flags=re.DOTALL
            ).strip()

            answer = response

        return answer
