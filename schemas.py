from typing import List
from pydantic import BaseModel


class Drug(BaseModel):
    pass


class User(BaseModel):
    username: str
    password: str


class SymptomData(BaseModel):
    symptoms: List[str]


class DiseaseData(BaseModel):
    disease: List[str]
