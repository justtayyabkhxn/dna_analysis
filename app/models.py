from pydantic import BaseModel
from typing import Optional


class GenerateSequenceRequest(BaseModel):
    sample_id: str


class CompareSequencesRequest(BaseModel):
    sample_id_1: str
    sample_id_2: str


class AskRequest(BaseModel):
    question: str


class UploadResponse(BaseModel):
    message: str
    total_records: int


class SequenceResponse(BaseModel):
    sample_id: str
    dna_sequence: str


class CompareResponse(BaseModel):
    sample_id_1: str
    sample_id_2: str
    similarity_score: float


class AskResponse(BaseModel):
    answer: str
