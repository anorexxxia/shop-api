from datetime import date, datetime

from enums import EnumGender
from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ClientOrm(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    client_name: Mapped[str] = mapped_column(String(length=50))
    client_surname: Mapped[str] = mapped_column(String(length=50))
    birthday: Mapped[date]
    gender: Mapped[EnumGender] = mapped_column(Enum(EnumGender, native_enum=True))
    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), init=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"), unique=True, init=False)

    address: Mapped["AddressOrm"] = relationship(back_populates="client", cascade="all, delete-orphan", single_parent=True)  # type: ignore # noqa: F821
