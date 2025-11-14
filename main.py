from aiogram import Dispatcher, Bot, flags
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import random

from database.session import SessionLocal
from database.crud import VocabularyWordCrud
from translation.gpt import translate_and_check
from utils import keyboard
from middleware.db import DBSessionMiddleware
from middleware.auth import AuthMiddleware, AuthLevel
import settings

bot = Bot(token=settings.TG_API_TOKEN)
dp = Dispatcher()
dp.update.middleware(DBSessionMiddleware(SessionLocal))
dp.message.middleware(AuthMiddleware())


@dp.message(CommandStart())
@flags.auth(level=AuthLevel.USER)
async def cmd_start(message: Message):
    await message.answer("Vocabulary bot. EN - SK")


@dp.message(Command(commands="add"))
@flags.auth(level=AuthLevel.USER)
async def cmd_add(message: Message, command: CommandObject, session: AsyncSession):
    word, translation = translate_and_check(command.args)
    vocab_word, created = await VocabularyWordCrud.get_or_create(
        session, word, translation, message.from_user.id
    )
    if not created:
        await message.answer(f"= {vocab_word.word} - {vocab_word.translations}")
        return
    await message.answer(f"+ {vocab_word.word} - {vocab_word.translations}")


@dp.message(Command(commands="quiz"))
@flags.auth(level=AuthLevel.USER)
async def quiz_cmd(message: Message, session: AsyncSession, state: FSMContext):
    await send_next_quiz(message, message.from_user.id, session, state)


@dp.message(Command(commands="list"))
@flags.auth(level=AuthLevel.USER)
async def list_cmd(message: Message, session: AsyncSession):
    words = await VocabularyWordCrud.words_list(session, message.from_user.id)
    if len(words) == 0:
        await message.answer("You don't have any words in vocabulary")
        return
    result = [f"{w.word} - {w.translations}" for w in words]
    await message.answer("\n".join(result))


@dp.callback_query()
async def handle_button_click(
    call: CallbackQuery, session: AsyncSession, state: FSMContext
):
    data = await state.get_data()
    question = call.message.text
    correct_answer = data.get("answer")
    user_answer = call.data
    result_text = []
    if user_answer == correct_answer:
        result_text.append(f"✅ You answered {user_answer}")
    else:
        result_text.append(f"❌ You answered /a{user_answer}")
    result_text.append(f"{question} - {correct_answer}")
    await call.answer()
    await call.message.answer("\n".join(result_text))
    await send_next_quiz(call.message, call.from_user.id, session, state)


async def send_next_quiz(
    message: Message, user_id: int, session: AsyncSession, state: FSMContext
):
    word, translations = await VocabularyWordCrud.random_word_with_fake_translations(
        session, user_id
    )
    if not word or len(translations) == 0:
        await message.answer("Vocabulary too small for quiz")
        return
    await state.update_data(answer=word.translations)
    translations = translations + [word.translations]
    random.shuffle(translations)
    await message.answer(
        word.word,
        reply_markup=keyboard.create_inline_keyboard(translations),
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
