# Telegram Bot with integrated RAG model
### Contents
- [Prerequisites]()
- [Managing dependencies]()
- [Starting the bot]()
- [Examples of how the bot works]()

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

## Examples of how the bot works