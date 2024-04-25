from flask import Flask, render_template, request
from py2neo import Graph

app = Flask(__name__)
graph = Graph("neo4j://localhost:7687", auth = ("neo4j", "keW3z48dcPHG8Au"))

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")
        selected_symptoms_query = ", ".join(f'"{symptom}"' for symptom in selected_symptoms)
        
        query = f"""
        MATCH (d:node)-[:симптом]->(s:Symptom)
        WHERE s.name IN [{selected_symptoms_query}]
        WITH d, COLLECT(s.name) AS allSymptoms, COUNT(DISTINCT s) AS numSymptoms
        WHERE numSymptoms = SIZE([{selected_symptoms_query}])
        RETURN d.name AS disease, allSymptoms AS symptoms
        """
        # MATCH (d:node)-[:симптом]->(s:Symptom)
        # WHERE s.name IN [{selected_symptoms_query}]
        # RETURN d.name AS disease, COLLECT(s.name) AS symptoms
        result = graph.run(query)
        diseases = [{"disease": record["disease"], "symptoms": record["symptoms"]} for record in result]
        return render_template("index.html", symptoms=get_all_symptoms(), selected_symptoms=selected_symptoms, diseases=diseases)
    
    return render_template("index.html", symptoms=get_all_symptoms(), selected_symptoms=[], diseases=[])

def get_all_symptoms():
    query = "MATCH (s:Symptom) RETURN s.name AS symptom"
    result = graph.run(query)
    return [record["symptom"] for record in result]
if __name__ == '__main__':
    app.run(debug=True)