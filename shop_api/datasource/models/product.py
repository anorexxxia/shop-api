from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ProductOrm(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(length=50))
    category: Mapped[str] = mapped_column(String(length=50))
    price: Mapped[Decimal] = mapped_column(Numeric(scale=2), CheckConstraint("price > 0", name="check_price_positive"))
    available_stock: Mapped[int] = mapped_column(CheckConstraint("available_stock >= 0", name="check_stock_not_negative")) 
    last_update_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), init=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id", ondelete="CASCADE"))
    image_id: Mapped[UUID | None] = mapped_column(ForeignKey("images.id", ondelete="SET NULL"), default=None)

    supplier: Mapped["SupplierOrm"] = relationship(back_populates="products", init=False)  # type: ignore # noqa: F821
    image: Mapped["ImagesOrm"] = relationship(back_populates="product", init=False, cascade="all, delete-orphan", single_parent=True)  # type: ignore # noqa: F821
