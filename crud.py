from neo4j import GraphDatabase


uri = 'bolt://localhost:7687'
user = "neo4j"
password = "keW3z48dcPHG8Au"

driver = GraphDatabase.driver(uri, auth=(user, password))


def get_session():
    session = driver.session()
    return session


class DbManager:

    def create(self):
        pass

    def read_all_symptoms(self):
        final_result = {}
        with (get_session() as session):
            result = session.run(
                #"MATCH (n:Symptom) RETURN n.name AS symptomName, n.description AS symptomDescription"
                "MATCH (n:Symptom) RETURN n.name AS symptomName,"
                " n.description AS symptomDescription, n.text AS symptomText"
            )
            for record in result:
                #final_result.update({record["symptomName"]: record["symptomDescription"]})
                final_result.update({record["symptomName"]: (record["symptomDescription"],
                                                             record["symptomText"])})
            return final_result

    def read_drug_by_substance(self, substance):
        query = f"""
                            MATCH (d:node)-[:активное_вещество]->(s:Symptom)
                            WHERE s.name IN [{selected_symptoms_query}]
                            WITH d, COLLECT(s.name) AS allSymptoms, COUNT(DISTINCT s) AS numSymptoms
                            WHERE numSymptoms = SIZE([{selected_symptoms_query}])
                            RETURN d.name AS disease, allSymptoms AS symptoms
                            """

        with get_session() as session:
            result = session.run(query)
            diseases = [{"disease": record["disease"], "symptoms": record["symptoms"]} for record in result]
            if diseases == []:
                return [{"disease": "No diseases found"}]
            else:
                return diseases

    def read_all_disease(self):
        with (get_session() as session):
            result = session.run("MATCH (d:node) RETURN d.name AS disease")
            return [record["disease"] for record in result]

    def read_one(self):
        pass

    def read_disease_by_symptom(self, selected_symptoms):
        selected_symptoms_query = ", ".join(f'"{symptom}"' for symptom in selected_symptoms.symptoms)
        query = f"""
                     MATCH (d:node)-[:симптом]->(s:Symptom)
                    WHERE s.name IN [{selected_symptoms_query}]
                    WITH d, COLLECT(s.name) AS allSymptoms, COUNT(DISTINCT s) AS numSymptoms
                    WHERE numSymptoms = SIZE([{selected_symptoms_query}])
                    RETURN d.name AS disease, allSymptoms AS symptoms
                    """

        with get_session() as session:
            result = session.run(query)
            diseases = [{"disease": record["disease"], "symptoms": record["symptoms"]} for record in result]
            if diseases == []:
                return [{"disease": "No diseases found"}]
            else:
                return diseases

    def read_by_name(self, name):
        with (get_session() as session):
            parameters = {name: 'name'}
            return session.run(f"MATCH (n) RETURN n", parameters).single()


class UserManager:
    def create_user(self, username: str, password: str):
        with get_session() as session:
            params = {'username': username, 'password': password}
            session.run("CREATE (u:User)",
                        parameters=params)

    def authenticate_user(self, username: str, password: str):
        with get_session() as session:
            params = {'username': username, 'password': password}
            result = session.run("SELECT (u:User)",
                        parameters=params)
        record = result.single()
        if record["username"] == username and record["password"] == password:
            return True
