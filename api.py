# --- Python Libraries ---
import uvicorn              # The server that runs our API
from fastapi import FastAPI # The API framework
from fastapi.middleware.cors import CORSMiddleware # To allow our React frontend to talk to this API
import sqlite3
import joblib
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel # For defining our admission data structure


DB_NAME = "universities.db"
CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "course_recommender"
MODEL_FILE = "admission_model.pkl"

print("Loading all models... This may take a moment.")
try:
    model_data = joblib.load(MODEL_FILE)
    admission_model = model_data['model']
    admission_model_features = model_data['features']
    print(f"Loaded admission model. Features: {admission_model_features}")

    
    recommender_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Loaded recommender embedding model.")

    
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    course_collection = client.get_collection(name=COLLECTION_NAME)
    print(f"Connected to vector database. Found {course_collection.count()} courses.")
    
except FileNotFoundError:
    print("----------------------------------------------------------------")
    print("!!! CRITICAL ERROR !!!")
    print("One or more model files not found. Did you run all Phase 1 scripts?")
    print(f"Missing: {MODEL_FILE} or {CHROMA_DB_PATH} or {DB_NAME}")
    print("----------------------------------------------------------------")
    exit()
except Exception as e:
    print(f"An error occurred during model loading: {e}")
    exit()

print("All models loaded successfully. Starting API...")

# Initialize the FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


class AdmissionQuery(BaseModel):
    grade: float
    language_level: str 

def query_db(query: str, params=()):
    """Helper function to run a SQL query and return a list of dictionaries."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row # This makes results easy to convert to JSON
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()



@app.get("/")
def read_root():
    """Welcome endpoint."""
    return {"message": "Welcome to the Uni-Navigator API!"}

@app.get("/courses")
def get_all_courses():
    """
    Fetches all courses and their university info from the SQL database.
    """
    query = """
    SELECT 
        c.course_id, 
        c.name AS course_name, 
        c.language, 
        c.description,
        u.name AS university_name, 
        u.city
    FROM courses c
    JOIN universities u ON c.university_id = u.university_id;
    """
    return query_db(query)

@app.get("/recommend_courses")
def recommend_courses(query: str):
    """
    Finds the 3 most similar courses based on a user's text query.
    (This is the RAG 'Retrieval' step)
    """
    print(f"Received recommendation query: {query}")
   
    query_embedding = recommender_model.encode(query).tolist()
    
    
    results = course_collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
   
    return results['metadatas'][0]

@app.post("/predict_chances")
def predict_chances(query: AdmissionQuery):
    """
    Predicts the admission chance based on a student's grade and language level.
    """
    print(f"Received prediction query: {query.dict()}")
    
   
    input_data = {
        'grade': [query.grade],
        'language_level_C1': [1 if query.language_level == 'C1' else 0],
        'language_level_C2': [1 if query.language_level == 'C2' else 0]
    }
    
    final_input = pd.DataFrame(columns=admission_model_features)
    final_input = pd.concat([final_input, pd.DataFrame(input_data)], ignore_index=True).fillna(0)
    
    final_input = final_input[admission_model_features]

    prediction_proba = admission_model.predict_proba(final_input)
    
    admit_chance = round(prediction_proba[0][1] * 100) 
    
    return {"admitted_chance_percent": admit_chance}

if __name__ == "__main__":
    print("Starting API server on http://127.0.0.1:8000")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)