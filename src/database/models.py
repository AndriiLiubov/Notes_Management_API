from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    versions = relationship(
        "NoteVersion", back_populates="note", cascade="all, delete-orphan"
    )


class NoteVersion(Base):
    __tablename__ = "note_versions"

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    note = relationship("Note", back_populates="versions")
