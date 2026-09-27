from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from forgeci.database import Base

#definition for a build structure
class Build(Base):
    __tablename__ = "builds"

    id: Mapped[int] = mapped_column(primary_key = True)
    repository: Mapped[str] = mapped_column(String(255))
    commit_sha: Mapped[str] = mapped_column(String(40))
    ref: Mapped[str] = mapped_column(String(255))

    status: Mapped[str] = mapped_column(
        String(50),
        default = "pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default = func.now()
    )
