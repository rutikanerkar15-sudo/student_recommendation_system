import sqlite3
import pandas as pd
import numpy as np

def init_db():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            topic TEXT,
            recommendation TEXT,
            feedback TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create student records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT,
            subject TEXT,
            topic TEXT,
            attendance_pct REAL,
            quiz_score REAL,
            exam_mark REAL
        )
    ''')
    
    # Populate initial synthetic data if table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        np.random.seed(42)
        n_records = 500
        
        student_ids = [f"STU{str(i).zfill(3)}" for i in np.random.randint(1, 101, size=n_records)]
        subjects = np.random.choice(['Mathematics', 'Physics', 'Computer Science', 'Chemistry'], size=n_records)
        attendance = np.random.uniform(50, 100, size=n_records).round(1)
        quiz_scores = np.random.uniform(40, 100, size=n_records).round(1)
        exam_marks = np.random.uniform(35, 98, size=n_records).round(1)
        
        topics_dict = {
            'Mathematics': ['Calculus', 'Linear Algebra', 'Probability', 'Trigonometry'],
            'Physics': ['Electromagnetism', 'Thermodynamics', 'Mechanics', 'Optics'],
            'Computer Science': ['Data Structures', 'Algorithms', 'Databases', 'Networking'],
            'Chemistry': ['Organic Reactions', 'Thermodynamics', 'Atomic Structure', 'Equilibrium']
        }
        
        topics = [np.random.choice(topics_dict[subj]) for subj in subjects]
        
        data = list(zip(student_ids, subjects, topics, attendance, quiz_scores, exam_marks))
        cursor.executemany('''
            INSERT INTO students (student_id, subject, topic, attendance_pct, quiz_score, exam_mark)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        print("Database initialized and populated with student records.")
        
    conn.commit()
    conn.close()

def save_feedback(student_id, topic, recommendation, feedback):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (student_id, topic, recommendation, feedback)
        VALUES (?, ?, ?, ?)
    ''', (student_id, topic, recommendation, feedback))
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM feedback", conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db()