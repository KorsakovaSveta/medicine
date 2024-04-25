from fastapi import FastAPI
from crud import DbManager
from schemas import SymptomData, DiseaseData

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
