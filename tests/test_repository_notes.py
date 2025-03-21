import pytest
from datetime import datetime
from src.database.models import Note, NoteVersion
from src.repository.notes import (
    create_note,
    get_all_notes,
    read_note,
    update_note,
    delete_note,
    get_note_versions,
)
from src.schemas import NoteModel
from fastapi.exceptions import HTTPException


def test_create_note(session):
    note_data = NoteModel(
        title="Test Note",
        content="This is a test note.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    note = create_note(session, note_data)

    assert note.id is not None
    assert note.title == "Test Note"
    assert note.content == "This is a test note."


def test_get_all_notes(session):
    notes = get_all_notes(skip=0, limit=10, db=session)
    assert isinstance(notes, list)


def test_read_note_success(session):
    note_data = NoteModel(
        title="Read Note",
        content="Content of read note",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    new_note = create_note(session, note_data)

    note = read_note(session, new_note.id)
    assert note.id == new_note.id
    assert note.title == "Read Note"


def test_read_note_not_found(session):
    with pytest.raises(HTTPException) as exc_info:
        read_note(session, 999)  # fake id

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Note not found"


def test_update_note(session):
    note_data = NoteModel(
        title="Update Test",
        content="Before update",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    new_note = create_note(session, note_data)

    update_data = NoteModel(
        title="Updated Title",
        content="After update",
        created_at=new_note.created_at,
        updated_at=datetime.now(),
    )
    response = update_note(session, new_note.id, update_data)

    assert response["message"] == "Note updated successfully"

    updated_note = read_note(session, new_note.id)
    assert updated_note.title == "Updated Title"
    assert updated_note.content == "After update"

    # check if versions created
    versions = get_note_versions(session, new_note.id)
    assert len(versions) == 1
    assert versions[0].title == "Update Test"


def test_update_note_not_found(session):
    update_data = NoteModel(
        title="Non-existent",
        content="Does not exist",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    with pytest.raises(HTTPException) as exc_info:
        update_note(session, 999, update_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Note not found"


def test_delete_note(session):
    note_data = NoteModel(
        title="Delete Test",
        content="This will be deleted",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    new_note = create_note(session, note_data)

    response = delete_note(session, new_note.id)
    assert response["message"] == "Note deleted"

    # check that there is no note
    with pytest.raises(HTTPException) as exc_info:
        read_note(session, new_note.id)

    assert exc_info.value.status_code == 404


def test_delete_note_not_found(session):
    with pytest.raises(HTTPException) as exc_info:
        delete_note(session, 999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Note not found"


def test_get_note_versions(session):
    note_data = NoteModel(
        title="Versioned Note",
        content="Original content",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    new_note = create_note(session, note_data)

    # make updates to create versions
    update_data = NoteModel(
        title="Version 2",
        content="Updated content",
        created_at=new_note.created_at,
        updated_at=datetime.now(),
    )
    update_note(session, new_note.id, update_data)

    update_data_2 = NoteModel(
        title="Version 3",
        content="Another update",
        created_at=new_note.created_at,
        updated_at=datetime.now(),
    )
    update_note(session, new_note.id, update_data_2)

    versions = get_note_versions(session, new_note.id)
    assert len(versions) == 2  # should be 2 versions
    assert versions[0].title == "Versioned Note"
    assert versions[1].title == "Version 2"
