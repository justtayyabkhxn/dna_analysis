# test_main.py

import io
import os
import pytest
from fastapi.testclient import TestClient

# adjust the import path if your main.py lives inside a folder
from app.main import app, data_store

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_data_store():
    # runs before each test
    data_store.clear()
    yield
    data_store.clear()

def test_upload_csv_and_count():
    csv_content = io.StringIO(
        "id,region,age,seed\n"
        "id_0001,latam,44,cgtacgtacgt\n"
        "id_0002,apac,60,agtcagtcagt\n"
    )
    response = client.post(
        "/upload-csv/",
        files={"file": ("remains.csv", csv_content.getvalue(), "text/csv")}
    )
    assert response.status_code == 200
    body = response.json()
    assert "parsed 2 records" in body["message"].lower()
    # data_store should now have two entries
    assert "id_0001" in data_store and "id_0002" in data_store

def test_generate_sequence_endpoint():
    # first upload
    csv_content = io.StringIO("id,region,age,seed\nid_0001,latam,44,cgtacgtacgt\n")
    client.post(
        "/upload-csv/",
        files={"file": ("remains.csv", csv_content.getvalue(), "text/csv")}
    )

    # now generate
    resp = client.get("/generate-sequence/", params={"id": "id_0001"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "id_0001"
    assert isinstance(data["sequence"], str)
    # sequence should be non-empty
    assert len(data["sequence"]) > 0

def test_compare_sequences_endpoint():
    # upload two samples
    csv = io.StringIO(
        "id,region,age,seed\n"
        "id_0001,latam,44,cgtacgtacgt\n"
        "id_0002,apac,60,agtcagtcagt\n"
    )
    client.post(
        "/upload-csv/",
        files={"file": ("remains.csv", csv.getvalue(), "text/csv")}
    )

    # compare
    resp = client.get("/compare-sequences/", params={"id1": "id_0001", "id2": "id_0002"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["id1"] == "id_0001" and body["id2"] == "id_0002"
    assert 0.0 <= body["similarity_score"] <= 1.0

@pytest.mark.skip(reason="Requires OpenAI key and network access")
def test_ask_me_anything_endpoint():
    # only run if you set OPENAI_API_KEY in your env
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No OpenAI key configured")
    payload = {"query": "What does this API do?"}
    resp = client.post("/ask-me-anything/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data and isinstance(data["response"], str)
