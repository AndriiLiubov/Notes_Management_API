from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.database.models import Note, NoteVersion
from src.schemas import NoteModel
from datetime import datetime

def create_note(db: Session, note: NoteModel):
    new_note = Note(
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_all_notes(skip: int, limit: int, db: Session):
    return db.query(Note).offset(skip).limit(limit).all()

def read_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

def update_note(db: Session, note_id: int, note_data: NoteModel):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Сохранение старой версии
    version = NoteVersion(
        note_id=note.id,
        title=note.title,
        content=note.content,
        created_at=datetime.now()
    )
    db.add(version)

    # Обновление заметки
    note.title = note_data.title
    note.content = note_data.content
    note.updated_at = datetime.now()
    
    db.commit()
    return {"message": "Note updated successfully"}

def delete_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}

def get_note_versions(db: Session, note_id: int):
    return db.query(NoteVersion).filter(NoteVersion.note_id == note_id).all()