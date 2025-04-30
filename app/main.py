from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from typing import Dict
import csv
import os

from app.func import generate_dna_sequence
from app.utils import compare_sequences, ask_openai_response

app = FastAPI(title="Ancient DNA Sequence Analyzer")

# Store data in-memory for simplicity
data_store: Dict[str, Dict] = {}

DATA_DIR = "app/data"
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Upload CSV Endpoint
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    
    content = await file.read()
    decoded = content.decode("utf-8").splitlines()

    reader = csv.DictReader(decoded)
    count = 0
    for row in reader:
        if row.get("id") and row.get("region") and row.get("age") and row.get("seed"):
            data_store[row["id"]] = {
                "region": row["region"],
                "age": int(row["age"]),
                "seed": row["seed"]
            }
            count += 1
    
    with open(os.path.join(DATA_DIR, "remains.csv"), "wb") as f:
        f.write(content)
    
    return {"message": f"Successfully uploaded and parsed {count} records."}


# 2. Generate DNA Sequence
@app.get("/generate-sequence/")
def generate_sequence(id: str = Query(..., description="ID of the ancient sample")):
    if id not in data_store:
        raise HTTPException(status_code=404, detail="Sample ID not found.")
    
    entry = data_store[id]
    sequence = generate_dna_sequence(
        id=id,
        region=entry["region"],
        age=entry["age"],
        seed=entry["seed"]
    )
    return {"id": id, "sequence": sequence}


# 3. Compare DNA Sequences
@app.get("/compare-sequences/")
def compare_sequences_api(id1: str, id2: str):
    if id1 not in data_store or id2 not in data_store:
        raise HTTPException(status_code=404, detail="One or both sample IDs not found.")
    
    seq1 = generate_dna_sequence(
        id=id1,
        region=data_store[id1]["region"],
        age=data_store[id1]["age"],
        seed=data_store[id1]["seed"]
    )
    seq2 = generate_dna_sequence(
        id=id2,
        region=data_store[id2]["region"],
        age=data_store[id2]["age"],
        seed=data_store[id2]["seed"]
    )

    score = compare_sequences(seq1, seq2)
    return {
        "id1": id1,
        "id2": id2,
        "similarity_score": score,
        "sequence_1": seq1,
        "sequence_2": seq2
    }


# 4. Ask Me Anything Endpoint
class Question(BaseModel):
    query: str

@app.post("/ask-me-anything/")
def ask_me_anything(payload: Question):
    response = ask_openai_response(payload.query)
    return {"question": payload.query, "response": response}
