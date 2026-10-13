from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class AddressOrm(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    country: Mapped[str] = mapped_column(String(length=50))
    city: Mapped[str] = mapped_column(String(length=100))
    street: Mapped[str] = mapped_column(String(length=100))

    supplier: Mapped["SupplierOrm"] = relationship(back_populates="address", init=False)  # type: ignore # noqa: F821
    client: Mapped["ClientOrm"] = relationship(back_populates="address", init=False)  # type: ignore # noqa: F821
