from database.model import VocabularyWord
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Tuple


class VocabularyWordCrud:
    @staticmethod
    async def get_by_word(
        sesion: AsyncSession, word: str, user_id: int
    ) -> VocabularyWord | None:
        stmt = (
            select(VocabularyWord)
            .where(VocabularyWord.word == word)
            .where(VocabularyWord.user_id == user_id)
        )
        return await sesion.scalar(stmt)

    @staticmethod
    async def get_or_create(
        sesion: AsyncSession, word: str, translation: str, user_id: int
    ):
        result = await VocabularyWordCrud.get_by_word(sesion, word, user_id)
        if result:
            return result, False

        result = VocabularyWord(word=word, translations=translation, user_id=user_id)
        sesion.add(result)
        await sesion.commit()
        await sesion.refresh(result)
        return result, True

    @staticmethod
    async def random_word_with_fake_translations(
        session: AsyncSession, user_id: int, fake_amount=3
    ) -> Tuple[VocabularyWord, List[str]]:
        word_stmt = (
            select(VocabularyWord)
            .where(VocabularyWord.user_id == user_id)
            .order_by(func.random())
            .limit(1)
        )
        word = await session.scalar(word_stmt)
        translation_stmt = (
            select(VocabularyWord.translations)
            .where(VocabularyWord.user_id == user_id)
            .order_by(func.random())
            .limit(fake_amount)
        )
        translations = await session.scalars(translation_stmt)
        return word, list(translations)

    @staticmethod
    async def words_list(session: AsyncSession, user_id: int) -> List[VocabularyWord]:
        stmt = select(VocabularyWord).where(VocabularyWord.user_id == user_id)
        return list(await session.scalars(stmt))
