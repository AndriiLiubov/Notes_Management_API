from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository import notes as note_repo
from src.services.aistudio import summarize_text
from src.schemas import NoteModel, NoteResponse, NoteVersionResponse
from typing import List

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteResponse)
def create_note(note: NoteModel, db: Session = Depends(get_db)):
    """
    Create a note.
    """
    return note_repo.create_note(db, note)


@router.get("/", response_model=List[NoteResponse])
def get_all_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get all notes.
    """
    return note_repo.get_all_notes(skip, limit, db)


@router.get("/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    """
    Get note by id.
    """
    return note_repo.read_note(db, note_id)


@router.put("/{note_id}", response_model=dict)
def update_note(note_id: int, note: NoteModel, db: Session = Depends(get_db)):
    """
    Update note by id.
    """
    return note_repo.update_note(db, note_id, note)


@router.delete("/{note_id}", response_model=dict)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Delete note by id.
    """
    return note_repo.delete_note(db, note_id)


@router.get("/{note_id}/versions/", response_model=List[NoteVersionResponse])
def get_note_versions(note_id: int, db: Session = Depends(get_db)):
    """
    Get note varsions by id.
    """
    return note_repo.get_note_versions(db, note_id)


@router.get("/{note_id}/summary/", response_model=dict)
def summarize_note(note_id: int, db: Session = Depends(get_db)):
    """
    Note summarization within Gemini AI.
    """
    note = note_repo.read_note(db, note_id)

    summary = summarize_text(note.content)
    return {"note_id": note_id, "summary": summary}
