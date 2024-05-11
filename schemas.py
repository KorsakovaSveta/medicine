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
    height_unit: str
    weight_unit: str


class ChildHeightCalculator(BaseModel):
    sex: str
    mother_height: int
    father_height: int
    mothers_height_unit: str
    fathers_height_unit: str
    height_potential_result_unit: str

class MeldnaCalculator(BaseModel):
    creatine: float
    bilirubin: float
    inr: float
    serum_na: float
    hemodialysis_twice_in_week_prior: float
    creatinine_unit: str
    bilirubin_unit: str
    serum_na_unit: str


class WaterCalculator(BaseModel):
    age_sex_factor: float
    desired_na: int
    normal_weight: float
    serum_na: int
    desired_na_unit: str
    normal_weight_unit: str
    serum_na_unit: str
    wdef_result_unit: str

