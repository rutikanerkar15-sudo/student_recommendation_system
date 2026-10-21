import sqlite3
import pandas as pd

class RecommendationEngine:
    def __init__(self):
        conn = sqlite3.connect('database.db')
        self.df = pd.read_sql_query("SELECT * FROM students", conn)
        conn.close()
        self.clean_data()

    def clean_data(self):
        self.df['attendance_pct'].fillna(self.df['attendance_pct'].median(), inplace=True)
        self.df['quiz_score'].fillna(self.df['quiz_score'].median(), inplace=True)
        self.df['exam_mark'].fillna(self.df['exam_mark'].median(), inplace=True)

    def identify_weak_areas(self, student_id):
        student_df = self.df[self.df['student_id'] == student_id]
        weak_rows = student_df[
            (student_df['exam_mark'] < 60) | 
            (student_df['quiz_score'] < 60) | 
            (student_df['attendance_pct'] < 75.0)
        ]
        return weak_rows

    def get_recommendations(self, topic):
        resource_mapping = {
            'Calculus': {'resource': 'Khan Academy Calculus Review Module', 'type': 'Video & Practice Quiz'},
            'Linear Algebra': 'MIT OCW Linear Algebra Lecture Notes & Exercises',
            'Probability': 'StatQuest Probability Fundamentals Guide',
            'Trigonometry': 'Interactive Trigonometric Identities Workshop',
            'Electromagnetism': 'HyperPhysics EM Field Summary & Practice Problems',
            'Thermodynamics': 'CrashCourse Physics: Laws of Thermodynamics',
            'Mechanics': 'Physics Classroom Newton Laws Tutorial',
            'Optics': 'Geometrical Optics Interactive Simulation Lab',
            'Data Structures': 'GeeksforGeeks Core Data Structures Practice Set',
            'Algorithms': 'LeetCode Easy-Medium Algorithmic Problem Set',
            'Databases': 'SQLZoo Interactive Database Tutorial',
            'Networking': 'Computer Networking Top-Down Approach Summary Notes',
            'Organic Reactions': 'Mastering Organic Chemistry Reaction Maps',
            'Atomic Structure': 'Khan Academy Atomic Structure & Periodic Table',
            'Equilibrium': 'ChemGuide Chemical Equilibrium Practice Questions'
        }
        return resource_mapping.get(topic, {'resource': 'General Subject Revision Workbook', 'type': 'PDF Guide'})