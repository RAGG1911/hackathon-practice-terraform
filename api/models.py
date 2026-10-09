from datetime import date, time, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    nombre_colegio: Mapped[str] = mapped_column(String(255))
    ubicacion: Mapped[str] = mapped_column(String(500))
    distrito: Mapped[str] = mapped_column(String(100))

    cantidad_estudiantes: Mapped[int] = mapped_column(Integer)

    dia: Mapped[date] = mapped_column(Date)
    hora: Mapped[time] = mapped_column(Time)

    nombre_persona: Mapped[str] = mapped_column(String(255))

    observacion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    latitud: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitud: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    photos: Mapped[list["Photo"]] = relationship(
        back_populates="visit",
        cascade="all, delete-orphan",
    )


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    visit_id: Mapped[int] = mapped_column(
        ForeignKey("visits.id", ondelete="CASCADE"),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    blob_name: Mapped[str] = mapped_column(
        String(500)
    )

    content_type: Mapped[str] = mapped_column(
        String(100)
    )

    url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    visit: Mapped["Visit"] = relationship(
        back_populates="photos"
    )