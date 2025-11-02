import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer
import os

DB_NAME = 'universities.db'
CHROMA_DB_PATH = 'chroma_db'
COLLECTION_NAME = 'course_recommender'

def load_course_description():
    """Fetches all course names and descriptions from the SQLite database."""
    if not os.path.exists(DB_NAME):
        print(f"Error: Database file '{DB_NAME}' not found.")
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT course_id, name, description FROM courses")
    courses = cursor.fetchall()
    conn.close()
    
    print(f"Successfully loaded {len(courses)} courses from the database.")
    return courses

def build_vector_database(courses):
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    documents = [course[2] for course in courses]
    metadatas = [{"course_name": course[1]} for course in courses]
    
    ids = [str(course[0]) for course in courses]
    
    embeddings = model.encode(documents, show_progress_bar=True)
    
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print("--- Vector Database Build Complete! ---")
    print(f"Database saved in folder: '{CHROMA_DB_PATH}'")
    print(f"Total documents in collection: {collection.count()}")
    
if __name__ == "__main__":
    course_data = load_course_description()
    if course_data:
        build_vector_database(course_data)