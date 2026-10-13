from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    pass

class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    firstname: Mapped[str] = mapped_column(String(length=50))
    lastname: Mapped[str] = mapped_column(String(length=50))
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str]
    password: Mapped[str]