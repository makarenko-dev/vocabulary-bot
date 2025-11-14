from typing import List
from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_inline_keyboard(values: List[str], columns=2):
    keyboard = InlineKeyboardBuilder()
    for val in values:
        keyboard.add(InlineKeyboardButton(text=val, callback_data=val))
    return keyboard.adjust(columns).as_markup()
