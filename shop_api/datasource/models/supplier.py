from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SupplierOrm(Base):
    __tablename__ = "supplier"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(length=100), unique=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"), unique=True, init=False)
    phone_number: Mapped[str] = mapped_column(String(length=20), unique=True)

    address: Mapped["AddressOrm"] = relationship(back_populates="supplier", cascade="all, delete-orphan", single_parent=True) # type: ignore  # noqa: F821
    products: Mapped[list["ProductOrm"]] = relationship(back_populates="supplier", init=False)  # type: ignore # noqa: F821