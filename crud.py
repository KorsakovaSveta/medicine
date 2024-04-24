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
        with (get_session() as session):
            result = session.run("MATCH (s:Symptom) RETURN s.name AS symptom")
            return [record["symptom"] for record in result]
    def read_all_disease(self):
        with (get_session() as session):
            result = session.run("MATCH (d:Disease) RETURN d.name AS disease")
            return [record["disease"] for record in result]
    def read_one(self):
        pass

    def read_disease_by_symptom(self, selected_symptoms):
        selected_symptoms_query = ", ".join(f'"{symptom}"' for symptom in selected_symptoms)
        query = f"""
                    MATCH (d:node)-[:симптом]->(s:Symptom)
                    WHERE s.name IN [{selected_symptoms_query}]
                    RETURN d.name AS disease, COLLECT(s.name) AS symptoms
                    """
        with get_session() as session:
            result = session.run(query)
            diseases = [{"disease": record["disease"], "symptoms": record["symptoms"]} for record in result]
            return diseases

class UserManager:
    def create_user(self, username: str, password: str):
        with get_session() as session:
            session.run("CREATE (u:User {username: $username, password_hash: $hashed_password})",
                username=username, password=password)

