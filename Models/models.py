from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


# Postagens do Twitter
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(String(50), unique=True)
    nome_portal: Mapped[str] = mapped_column(String(15))
    texto_postagem: Mapped[str] = mapped_column()
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    def __repr__(self):
        return f"[Post {self.id}] @{self.nome_portal}: {self.texto_postagem[:140]}... link [{self.link}]"


# Comentários das Postagens
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(15))
    comment: Mapped[str] = mapped_column(String(280))

    # Adicionamos a chave estrangeira que aponta para o id da tabela 'posts'
    post_id : Mapped[str] = mapped_column(ForeignKey("posts.link"))

    # Corrigimos o back_populates para 'comments'
    post: Mapped["Post"] = relationship(back_populates="comments")

    def __repr__(self):
        return f"@{self.user} comentou: {self.comment[:140]}... no post {self.post.__repr__()}"