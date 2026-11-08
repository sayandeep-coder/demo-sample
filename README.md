# 🧠 Gemini 2.5 Flash + LangChain Knowledge Base Chat System

A knowledge base chat system powered directly by **Google Gemini 2.5 Flash** (`gemini-2.5-flash`) and **LangChain**, utilizing the model's vast pre-trained global knowledge base with an interactive CLI interface.

---

## ✨ Features

- ⚡ **Gemini 2.5 Flash (`gemini-2.5-flash`)**: Answers any question using its comprehensive pre-trained world knowledge.
- 🔗 **LangChain Pipeline**: `ChatGoogleGenerativeAI` integrated with `ChatPromptTemplate` and conversational history.
- 💬 **Interactive CLI**:
  - Live conversational chat with memory across turns.
  - Commands: `/help`, `/clear`, `/exit`.
  - Direct single-query mode: `python cli.py -q "<question>"`.

---

## 🚀 How to Run

### Interactive CLI Chat:
```bash
python cli.py
```
*(or `python main.py`)*

### Single-Query Mode:
```bash
python cli.py -q "tell me about Rothas"
python cli.py -q "tell me about hit haldia"
```
