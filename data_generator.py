import sqlite3
import random 
import os

DB_NAME = "universities.db"

universities = [
   ("Technische Universität München (TUM)", "München", "Bayern"),
    ("Ludwig-Maximilians-Universität München (LMU)", "München", "Bayern"),
    ("Rheinisch-Westfälische Technische Hochschule Aachen (RWTH)", "Aachen", "Nordrhein-Westfalen"),
    ("Freie Universität Berlin (FU Berlin)", "Berlin", "Berlin"),
    ("Humboldt-Universität zu Berlin (HU Berlin)", "Berlin", "Berlin"),
    ("Karlsruher Institut für Technologie (KIT)", "Karlsruhe", "Baden-Württemberg"),
    ("Universität Heidelberg", "Heidelberg", "Baden-Württemberg"),
    ("Technische Universität Berlin (TU Berlin)", "Berlin", "Berlin"),
    ("Universität Hamburg", "Hamburg", "Hamburg"),
    ("Goethe-Universität Frankfurt am Main", "Frankfurt", "Hessen"),
    ("Technische Universität Darmstadt", "Darmstadt", "Hessen") 
]
courses = [
    (1, "B.Sc. Informatik", "German", "Ein fundamentaler Kurs, der alle Aspekte der modernen Informatik abdeckt, von Software-Engineering bis hin zu KI."),
    (1, "B.Sc. Maschinenbau", "German", "Klassischer Maschinenbau mit Fokus auf Robotik, Fahrzeugtechnik und Produktion."),
    (1, "M.Sc. Data Science", "English", "An advanced, English-taught program focusing on machine learning, big data, and statistical analysis."),
    (2, "B.A. Betriebswirtschaftslehre (BWL)", "German", "Ein umfassendes BWL-Studium mit Schwerpunkten in Finanzen und Marketing."),
    (2, "M.Sc. Physics", "English", "Covers theoretical and experimental physics, with options to specialize in astrophysics or quantum mechanics."),
    (3, "B.Sc. Elektrotechnik", "German", "Fokussiert auf Informationstechnik und Mikroelektronik."),
    (3, "M.Sc. Automotive Engineering", "English", "A world-renowned program for automotive systems, connected driving, and e-mobility."),
    (4, "B.A. Politikwissenschaft", "German", "Analyse von politischen Systemen, internationalen Beziehungen und politischer Theorie."),
    (5, "B.Sc. Biologie", "German", "Umfassende Ausbildung in Molekularbiologie, Ökologie und Genetik."),
    (6, "B.Sc. Wirtschaftsingenieurwesen", "German", "Eine interdisziplinäre Ausbildung, die Ingenieurwesen mit Betriebswirtschaft verbindet."),
    (7, "B.A. Medizin (Modellstudiengang)", "German", "Innovatives Medizinstudium mit starkem Praxisbezug ab dem ersten Semester."),
    (8, "M.Sc. Computer Science", "English", "International master's program with a focus on data analytics and human-computer interaction."),
    (9, "M.Sc. International Business and Economics", "English", "A program designed for understanding global markets and economic policies."),
    (10, "B.Sc. Rechtswissenschaften (Jura)", "German", "Das klassische Jurastudium, das auf das erste Staatsexamen vorbereitet.")
]

requirements = [
    (1, 2.0, "C1"),
    (2, 2.5, "C1"),
    (3, 1.7, "C1"), 
    (4, 2.3, "C1"),
    (5, 1.9, "C1"),
    (6, 2.4, "C1"),
    (7, 1.3, "C1"),
    (8, 2.1, "C1"),
    (9, 2.2, "C1"),
    (10, 2.8, "C1"),
    (11, 1.2, "C1"),
    (12, 1.8, "C1"),
    (13, 2.0, "C1"),
    (14, 2.5, "C1")
]

def create_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
                   CREATE TABLE universities (
                       university_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       city TEXT,
                       state TEXT)
                       
                """)    
    print("Table university created")
    
    cursor.execute( """
                   CREATE TABLE courses(
                       course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       university_id INTEGER,
                       name TEXT NOT NULL,
                       language TEXT,
                       description TEXT,
                       FOREIGN KEY (university_id) REFERENCES universities (university_id))
                       """)
    
    cursor.execute("""
                   CREATE TABLE requirements(
                       requirement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       course_id INTEGER,
                       required_grade REAL,
                       language_level TEXT,
                       FOREIGN KEY (course_id) REFERENCES courses (course_id)
                       )
                       """)
    print("table requirements created")
    
    
    try:
        cursor.executemany("INSERT INTO universities (name, city, state) VALUES (?, ?, ?)", universities)
        print(f"Inserted {len(universities)} universities")
        
        cursor.executemany("INSERT INTO courses (university_id, name, language, description) VALUES (?, ?, ?, ?)", courses)
        print(f"Inserted {len(courses)} courses.")
        
        cursor.executemany("INSERT INTO requirements (course_id, required_grade, language_level) VALUES (?, ?, ?)", requirements)
        print(f"Inserted {len(requirements)} requirements.")
        
        conn.commit()
        print("All data successfully committed.")
    except Exception as e:
       print(f"An error occurred while inserting data: {e}")
       conn.rollback()

       
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    create_database()    
