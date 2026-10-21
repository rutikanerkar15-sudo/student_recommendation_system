🎓 AI-Based Student Performance & Learning Recommendation System
An interactive analytics web application built with Python and Streamlit that evaluates student assessment results, attendance records, and quiz scores to identify knowledge gaps and recommend targeted learning resources.

🚀 Key Features
Student Performance Portal:

Individualized student profile views showing subject-wise marks, quiz results, and attendance metrics.

Interactive performance charts powered by Plotly.

Automated detection of weak learning topics using transparent rule-based logic.

Tailored learning resource recommendations (videos, practice sets, documentation) with a feedback loop (👍 Useful / 👎 Not Useful).

Teacher & Administrator Dashboard:

Class-wide performance and attendance distributions.

Real-time identification of at-risk students who require immediate academic support.

Analytics tracking for student feedback on recommendations.

Database Backend: Uses SQLite for secure local persistence of student metrics and user feedback.

🛠️ Tech Stack
Language: Python

Web Framework: Streamlit

Data Manipulation & Analysis: Pandas, NumPy

Data Visualization: Plotly

Database: SQLite

Machine Learning / Analytics: scikit-learn (baseline evaluation rules)

📁 Project Directory Structure
Plaintext
student_recommendation_system/
│
├── venv/                 # Virtual environment folder
├── database.py           # SQLite database initialization & helper functions
├── model.py              # Data cleaning & recommendation rule engine
├── app.py                # Main Streamlit dashboard application
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
⚙️ Installation & Quickstart Guide
Follow these steps to set up and run the project locally on your machine:

1. Clone or Open Project Folder
Open your terminal (PowerShell on Windows) and navigate to your project directory:

PowerShell
cd path\to\student_recommendation_system
2. Create and Activate Virtual Environment
PowerShell
python -m venv venv
venv\Scripts\Activate.ps1
(Note: If PowerShell blocks script execution, run Set-ExecutionPolicy Unrestricted -Scope Process first).

3. Install Dependencies
PowerShell
pip install -r requirements.txt
4. Initialize the SQLite Database
Run the database script to create tables and seed synthetic student records:

PowerShell
python database.py
5. Launch the Streamlit App
Run the dashboard application:

PowerShell
streamlit run app.py

github link : https://github.com/rutikanerkar15-sudo/student_recommendation_system
