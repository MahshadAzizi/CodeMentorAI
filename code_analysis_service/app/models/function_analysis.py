import json

from sqlalchemy import String, func, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from code_analysis_service.app.config.db import Base


class FunctionAnalysis(Base):
    __tablename__ = 'function_analysis'

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey('job.id'),
    )

    job = relationship(
        'Job',
        back_populates='functions',
    )

    function_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    function_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    suggestions: Mapped[json] = mapped_column(
        JSON,
        nullable=False
    )

    created_at = mapped_column(
        DateTime,
        default=func.now(),
    )
