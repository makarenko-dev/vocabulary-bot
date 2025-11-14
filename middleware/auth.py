from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag, extract_flags
from enum import Enum

import settings


class AuthLevel(Enum):
    UNKNOWN = 0
    USER = 1
    ADMIN = 2


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        self._user_storage = [int(uid) for uid in settings.USER_IDS.split(",")]

    async def __call__(self, handler, event, data):
        authorization = get_flag(data, "auth")
        if authorization is not None:
            level = authorization.get("level")
            if event.chat.id in self._user_storage:
                return await handler(event, data)
            await event.answer(
                f"Bot is working only for friends. Contect admin and say that your id = {event.chat.id}"
            )
            return None
        return await handler(event, data)
