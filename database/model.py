from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer


class Base(DeclarativeBase):
    pass


class VocabularyWord(Base):
    __tablename__ = "vocabulary_word"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer(), index=True)
    word: Mapped[str] = mapped_column(String(100))
    translations: Mapped[str] = mapped_column(String(200))
