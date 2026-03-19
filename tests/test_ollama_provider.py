import asyncio
import json
import tempfile

import pytest

from app.llm.providers.ollama import OllamaProvider, OCRRequest


class DummyResponse:
    def __init__(self, status: int, body: str):
        self.status = status
        self._body = body

    # make this object usable with "async with" in the provider
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # nothing special on exit
        return False

    async def text(self):
        return self._body

    async def json(self):
        # simulate JSON wrapper around text
        return {"output": self._body}


class DummySession:
    def __init__(self, resp: DummyResponse):
        self._resp = resp

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    # session.post should return an object usable in "async with" directly,
    # so we make this a normal method rather than a coroutine.
    def post(self, *args, **kwargs):
        return self._resp


@pytest.mark.asyncio
async def test_ollama_json_parsing(monkeypatch, tmp_path):
    # create a temporary file to represent the document
    doc_path = tmp_path / "doc.pdf"
    doc_path.write_bytes(b"dummy data")

    provider = OllamaProvider()

    # prepare fake JSON from model
    fake_json = '{"invoice_number": "INV-123", "invoice_date": "2026-02-27", "total_amount": "100.00"}'
    dummy_resp = DummyResponse(status=200, body=fake_json)
    monkeypatch.setattr("aiohttp.ClientSession", lambda: DummySession(dummy_resp))

    res = await provider.process_ocr(OCRRequest(document_path=str(doc_path), document_type="INVOICE"))

    assert res.status == "success"
    inv_field = res.fields.get("invoice_number")
    assert inv_field is not None and inv_field.value == "INV-123"
    total_field = res.fields.get("total_amount")
    assert total_field is not None and total_field.value == "100.00"
    # raw_response should contain the JSON text
    assert fake_json in res.raw_response["body"]
