import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch
from src.database.models import Note
from src.schemas import NoteModel
from src.repository import notes as note_repo
from unittest.mock import patch, MagicMock
from src.services.aistudio import summarize_text


def test_create_note(client: TestClient, session: Session, note: dict):
    response = client.post("/notes/", json=note)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == note["title"]
    assert data["content"] == note["content"]
    assert "id" in data


def test_get_all_notes(client: TestClient, session: Session, note: dict):
    response = client.get("/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_note(client: TestClient, session: Session, note: dict):
    # Создаем заметку
    response = client.post("/notes/", json=note)
    note_id = response.json()["id"]

    # Получаем её по ID
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == note["title"]
    assert data["content"] == note["content"]


def test_update_note(client: TestClient, session: Session, note: dict):
    # Создаем заметку
    response = client.post("/notes/", json=note)
    note_id = response.json()["id"]

    updated_note = {"title": "Updated title", "content": "Updated content"}

    # Обновляем заметку
    response = client.put(f"/notes/{note_id}", json=updated_note)
    assert response.status_code == 200
    assert response.json()["message"] == "Note updated successfully"

    # Проверяем обновленную заметку
    response = client.get(f"/notes/{note_id}")
    data = response.json()
    assert data["title"] == updated_note["title"]
    assert data["content"] == updated_note["content"]


def test_delete_note(client: TestClient, session: Session, note: dict):
    # Создаем заметку
    response = client.post("/notes/", json=note)
    note_id = response.json()["id"]

    # Удаляем заметку
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Note deleted"

    # Проверяем, что заметки больше нет
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404


def test_get_note_versions(client: TestClient, session: Session, note: dict):
    response = client.get("/notes/1/versions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@patch("google.generativeai.GenerativeModel.generate_content")
def test_summarize_note(mock_generate_content, client, session, note):
    # Подготовка тестовых данных
    response = client.post("/notes/", json=note)
    note_id = response.json()["id"]

    # Настраиваем поведение мокнутого метода
    mock_generate_content.return_value.text = "Short summary"

    # Отправляем запрос на эндпоинт
    response = client.get(f"/notes/{note_id}/summary/")

    # Проверяем статус код
    assert response.status_code == 200

    # Проверяем ответ
    assert response.json() == {"note_id": note_id, "summary": "Short summary"}

    # Убеждаемся, что mock вызвался один раз
    mock_generate_content.assert_called_once()
