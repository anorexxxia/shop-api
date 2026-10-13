import uuid

from sqlalchemy import LargeBinary, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ImagesOrm(Base):
    __tablename__ = "images"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), init=False)
    image: Mapped[bytes] = mapped_column(LargeBinary)

    product: Mapped["ProductOrm"] = relationship(back_populates="image", init=False)  # type: ignore # noqa: F821
