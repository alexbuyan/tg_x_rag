# Telegram Bot with integrated RAG model
### Contents
- [Prerequisites](https://github.com/alexbuyan/tg_x_rag/tree/readme?tab=readme-ov-file#prerequisites)
- [Managing dependencies](https://github.com/alexbuyan/tg_x_rag/tree/readme?tab=readme-ov-file#managing-dependencies)
- [Starting the bot](https://github.com/alexbuyan/tg_x_rag/tree/readme?tab=readme-ov-file#starting-the-bot)
- [Examples of how the bot works](https://github.com/alexbuyan/tg_x_rag/tree/readme?tab=readme-ov-file#examples-of-how-the-bot-works)

## Prerequisites
- Install [Ollama](https://ollama.com/) locally on your computer
- Download `llama3`
```bash
ollama pull llama3
```
- Create `.env` file and specify `BOT_TOKEN`

## Managing dependencies
The project uses poetry to manage dependencies. To install all the dependencies use these commands:
```bash
poetry install --no-root
```

## Starting the bot
```bash
poetry shell
cd tg_x_rag
python bot.py
```
### Commands
```
/load_doc -- add PDF document to the RAG model
/clear_docs -- delete all documents from the RAG model memory
/chat -- start chatting with the model (start the infinite loop)
/cancel -- cancel the current chat loop
```

## Examples of how the bot works
![](examples/tg_interaction.mov)