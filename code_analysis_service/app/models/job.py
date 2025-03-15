import enum

from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from code_analysis_service.app.config.db import Base


class JobStatus(enum.Enum):
    PENDING = "PENDING"
    DOWNLOADING = "DOWNLOADING"
    DONE = "DONE"
    FAILED = "FAILED"


class Job(Base):
    __tablename__ = 'job'

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    uuid: Mapped[UUID] = mapped_column(
        UUID,
        nullable=False
    )

    functions = relationship(
        'FunctionAnalysis',
        back_populates='job',
    )

    repo_url: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    local_path: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at = mapped_column(
        DateTime,
        default=func.now(),
    )

    updated_at = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )
