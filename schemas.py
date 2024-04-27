from typing import List
from pydantic import BaseModel


class Drug(BaseModel):
    pass


class User(BaseModel):
    username: str
    password: str


class SymptomInput(BaseModel):
    symptoms: List[str]


class SymptomData(BaseModel):
    symptoms: dict


class DiseaseData(BaseModel):
    disease: List[str]


class BmiCalculator(BaseModel):
    height: int
    weight: float


class ChildHeightCalculator(BaseModel):
    sex: str
    mother_height: int
    father_height: int


class MeldnaCalculator(BaseModel):
    creatine: float
    bilirubin: float
    inr: float
    serum: float
    hemodialysis: bool


class WaterCalculator(BaseModel):
    age_sex_factor: float
    desired: int
    normal_weight: float
    serum: int
