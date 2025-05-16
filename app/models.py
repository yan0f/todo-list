from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy.orm import Mapped, mapped_column


class Task(BigIntAuditBase):
    __tablename__ = 'tasks'

    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]
    completed: Mapped[bool] = mapped_column(default=False)
