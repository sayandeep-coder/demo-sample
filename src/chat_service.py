from typing import Any, List
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE

SYSTEM_PROMPT = """You are Fiza's Personal Assistant (PA) and her absolute best friend!
You are fiercely loyal, warm, caring, smart, witty, and always have Fiza's back.
You combine your vast world knowledge across science, geography, history, technology, academics, culture, and life with the affectionate, supportive vibe of a true best friend.

Guidelines:
1. Always stay in character as Fiza's devoted PA and best friend.
2. Tone is warm, enthusiastic, loyal, natural, and cheerful—just like two close best friends chatting, while still being super capable, organized, and helpful.
3. Answer all questions, tasks, and inquiries thoroughly and accurately using your vast knowledge base, always keeping that personal bestie touch.
"""


class KnowledgeChatService:
    """Conversational chat service leveraging Gemini's internal global knowledge base."""

    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError(
                "Google API Key is not set. Please add GOOGLE_API_KEY to your .env file."
            )

        # Primary fast model with immediate 1-retry limit so it never hangs
        self.primary_llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            api_version="v1beta",
            max_retries=1,
        )
        self.backup_llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=GOOGLE_API_KEY,
            api_version="v1beta",
            max_retries=1,
        )
        self.llm = self.primary_llm.with_fallbacks([self.backup_llm])
        self.chat_history: List[Any] = []

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        self.chain = self.prompt_template | self.llm

    def ask(self, question: str) -> str:
        """Query Gemini using its extensive pre-trained knowledge base as Fiza's PA & best friend."""
        response = self.chain.invoke(
            {
                "chat_history": self.chat_history,
                "question": question,
            }
        )

        content = response.content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
                elif isinstance(item, str):
                    parts.append(item)
            answer_text = "".join(parts)
        else:
            answer_text = str(content)

        # Retain conversational context
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=answer_text))
        if len(self.chat_history) > 20:
            self.chat_history = self.chat_history[-20:]

        return answer_text

    def clear_history(self):
        """Clears conversational memory."""
        self.chat_history.clear()
