from fastapi import FastAPI
from crud import DbManager
from schemas import SymptomData, DiseaseData, BmiCalculator, ChildHeightCalculator, MeldnaCalculator, WaterCalculator

app = FastAPI(debug=True)
db_manager = DbManager()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get_disease")
async def selected_disease(selected_symptoms: SymptomData):
    result = db_manager.read_disease_by_symptom(selected_symptoms)
    diseases = [item['disease'] for item in result]
    disease = DiseaseData(disease=diseases)
    return disease.model_dump_json()


@app.get("/get_all_symptoms")
async def all_symptoms():
    symptoms = SymptomData(symptoms=db_manager.read_all_symptoms())
    return symptoms.model_dump_json()


@app.get("/get_all_disease")
async def all_disease():
    disease = DiseaseData(disease=db_manager.read_all_disease())
    return disease.model_dump_json()


@app.get("/med_calc/bmi")
async def BmiCalculator(calc: BmiCalculator):
    example = 52
    return {"result": {example}}


@app.get("/med_calc/child_height")
async def ChildHeightCalculator(calc: ChildHeightCalculator):
    example = 52
    return {"potential": {example}, "z_score": {example}, "percentile": {example}}


@app.get("/med_calc/meldna")
async def MeldnaCalculator(calc: MeldnaCalculator):
    example = 52
    return {"meld_score": {example}, "meldna_score": {example}}


@app.get("/med_calc/water")
async def WaterCalculator(calc: WaterCalculator):
    example = 52
    return {"result": {example}}
