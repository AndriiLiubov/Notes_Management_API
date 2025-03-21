from sqlalchemy.orm import Session
from src.database.models import Note


def get_all_notes(db: Session):
    return db.query(Note).all()
