
import os
import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ocr_success(monkeypatch):
    # Simula o TesseractAPI para não depender de modelo real
    class DummyOCR:
        def __init__(self, *args, **kwargs):
            pass
        def transcribe(self, image_bytes):
            return False, False, "Texto de teste"
    monkeypatch.setattr("app.api.ocr.TesseractAPI", DummyOCR)
    img_bytes = b"fake-image-bytes"
    response = client.post("/ocr", files={"file": ("test.png", io.BytesIO(img_bytes), "image/png")})
    assert response.status_code == 200
    assert response.json()["text"] == "Texto de teste"
    assert "low_confidence" in response.json()

def test_ocr_invalid_file():
    response = client.post("/ocr", files={"file": ("test.txt", io.BytesIO(b"not-an-image"), "text/plain")})
    assert response.status_code == 400
    assert "imagem" in response.json()["detail"].lower()

def test_ocr_internal_error(monkeypatch):
    class DummyOCR:
        def __init__(self, *args, **kwargs):
            pass
        def transcribe(self, image_bytes):
            raise RuntimeError("Erro interno")
    monkeypatch.setattr("app.api.ocr.TesseractAPI", DummyOCR)
    img_bytes = b"fake-image-bytes"
    response = client.post("/ocr", files={"file": ("test.png", io.BytesIO(img_bytes), "image/png")})
    assert response.status_code == 500
    assert "erro ao processar" in response.json()["detail"].lower()
