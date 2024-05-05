from fastapi import FastAPI
from crud import DbManager, UserManager
from schemas import SymptomData, DiseaseData, BmiCalculator, ChildHeightCalculator, MeldnaCalculator, WaterCalculator, \
    SymptomInput
from math import sqrt, erf

app = FastAPI(debug=True)
db_manager = DbManager()
user_manager = UserManager()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get_disease")
async def selected_disease(selected_symptoms: SymptomInput):
    result = db_manager.read_disease_by_symptom(selected_symptoms)
    diseases = [item['disease'] for item in result]
    disease = DiseaseData(disease=diseases)
    return selected_symptoms, disease.model_dump_json()


@app.get("/get_all_symptoms")
async def all_symptoms():
    symptoms = SymptomData(symptoms=db_manager.read_all_symptoms())
    return symptoms.model_dump_json()


@app.get("/get_all_disease")
async def all_disease():
    disease = DiseaseData(disease=db_manager.read_all_disease())
    return disease.model_dump_json()


@app.get("/search")
async def search(name: str):
    return db_manager.read_by_name(name)


@app.post("/med_calc/bmi")
async def BmiCalculator(calc: BmiCalculator):
    height = calc.height
    weight = calc.weight
    height_unit = calc.height_unit
    weight_unit = calc.weight_unit

    height_factors = {
        'cm': 1,
        'inch': 2.54,
        'in': 2.54,
        'mm': 0.1,
        'm': 100
    }

    weight_factors = {
        'gm': 0.001,
        'kg': 1,
        'lb': 0.453592
    }

    height_meters = height * height_factors[height_unit.lower()]
    weight_kg = weight * weight_factors[weight_unit.lower()]
    bmi = (weight_kg / (height_meters ** 2) * 10000)
    bmi = round(bmi, 2)
    return bmi


@app.post("/med_calc/child_height")
async def ChildHeightCalculator(calc: ChildHeightCalculator):
    def z_to_percentile(z_score):
        return round((1 + erf(z_score / sqrt(2))) * 50, 2)

    sex = calc.sex
    mothers_height = calc.mothers_height
    fathers_height = calc.fathers_height
    mothers_height_unit = calc.mothers_height_unit
    fathers_height_unit = calc.fathers_height_unit
    height_potential_result_unit = calc.height_potential_result_unit

    if mothers_height_unit == "inch" or mothers_height_unit == "in":
        mothers_height_cm = mothers_height * 2.54
    elif mothers_height_unit == "mm":
        mothers_height_cm = mothers_height / 10
    elif mothers_height_unit == "m":
        mothers_height_cm = mothers_height * 100
    else:
        mothers_height_cm = mothers_height

    if fathers_height_unit == "inch" or fathers_height_unit == "in":
        fathers_height_cm = fathers_height * 2.54
    elif fathers_height_unit == "mm":
        fathers_height_cm = fathers_height / 10
    elif fathers_height_unit == "m":
        fathers_height_cm = fathers_height * 100
    else:
        fathers_height_cm = fathers_height

    if sex == "Female":
        target_height_cm = ((fathers_height_cm - 13) + mothers_height_cm) / 2
    elif sex == "Male":
        target_height_cm = ((mothers_height_cm + 13) + fathers_height_cm) / 2
    else:
        return "Invalid sex"

    if sex == "Female":
        L = 1.108046193
        M = 163.338251
        S = 0.039636316
    elif sex == "Male":
        L = 1.167279219
        M = 176.8492322
        S = 0.040369574
    else:
        return "Invalid sex"

    z_score = ((target_height_cm / M) ** L - 1) / (L * S)
    z_score = round(z_score, 2)
    height_percentile = z_to_percentile(z_score)
    if height_potential_result_unit == "inch" or height_potential_result_unit == "in":
        height_potential_result = target_height_cm / 2.54
    elif height_potential_result_unit == "mm":
        height_potential_result = target_height_cm * 10
    elif height_potential_result_unit == "m":
        height_potential_result = target_height_cm / 100
    else:
        height_potential_result = target_height_cm

    height_potential_result = round(height_potential_result, 2)
    return {"height_potential": height_potential_result, "z-score": z_score, "height_percentile": height_percentile}




@app.post("/med_calc/meldna")
async def MeldnaCalculator(calc: MeldnaCalculator):
    example = 52
    return {"meld_score": {example}, "meldna_score": {example}}


@app.post("/med_calc/water")
async def WaterCalculator(calc: WaterCalculator):
    example = 52
    return {"result": {example}}

@app.post("/signup")
async def signup(username: str, password: str):
    user_manager.create_user(username, password)
    return {"message": "User created successfully"}

@app.get("/login")
async def login(username: str, password: str):
    if user_manager.authenticate_user(username, password):
        return {"message": "Authentication successfully"}

