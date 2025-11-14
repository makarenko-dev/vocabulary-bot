# vocabulary-bot
Telegram bot that acts as vocabulary. Used for studing Slovak language.
Supports adding new words (auto translates), printing all saved words, quizing.
OpenAI used for check spelling / translating during add phaze

## Build
- Fill .env file (all variables can be found in settings.py)
```
pip install -r requirements.txt
alembic upgrade head
```