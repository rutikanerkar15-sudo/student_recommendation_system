import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, save_feedback, get_all_feedback
from model import RecommendationEngine

# Initialize Database & Tables
init_db()

@st.cache_resource
def load_engine():
    return RecommendationEngine()

engine = load_engine()

st.set_page_config(page_title="Student Learning Recommendation System", layout="wide")

st.title("🎓 AI-Based Student Performance & Learning Recommendation System")
st.markdown("---")

# Role Selection Sidebar
st.sidebar.header("Access Control & Navigation")
role = st.sidebar.selectbox("Select Role", ["Student Portal", "Teacher / Admin Portal"])

if role == "Student Portal":
    st.sidebar.markdown("---")
    student_list = sorted(engine.df['student_id'].unique().tolist())
    selected_student = st.sidebar.selectbox("Select Your Student ID", student_list)
    
    st.header(f"Performance Profile: {selected_student}")
    
    student_data = engine.df[engine.df['student_id'] == selected_student]
    
    # Metrics Overview
    col1, col2, col3 = st.columns(3)
    avg_exam = student_data['exam_mark'].mean()
    avg_quiz = student_data['quiz_score'].mean()
    avg_attendance = student_data['attendance_pct'].mean()
    
    col1.metric("Average Exam Mark", f"{avg_exam:.1f}%")
    col2.metric("Average Quiz Score", f"{avg_quiz:.1f}%")
    col3.metric("Overall Attendance", f"{avg_attendance:.1f}%")
    
    st.markdown("### Subject-Wise Performance Trends")
    fig = px.bar(student_data, x='subject', y=['exam_mark', 'quiz_score'], barmode='group',
                 labels={'value': 'Score (%)', 'variable': 'Assessment Type'},
                 title="Exam & Quiz Scores by Subject")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Targeted Support & Recommendations")
    weak_topics = engine.identify_weak_areas(selected_student)
    
    if weak_topics.empty:
        st.success("🎉 Excellent work! You have no flagged weak topics currently. Keep up the consistent performance!")
    else:
        st.warning(f"Identified {len(weak_topics)} topic(s) requiring revision support.")
        for idx, row in weak_topics.iterrows():
            rec = engine.get_recommendations(row['topic'])
            rec_text = rec['resource'] if isinstance(rec, dict) else rec
            
            with st.expander(f"Topic: {row['topic']} ({row['subject']}) — Exam Mark: {row['exam_mark']}%"):
                st.write(f"**Recommended Resource:** {rec_text}")
                col_fb1, col_fb2 = st.columns(2)
                if col_fb1.button("👍 Useful", key=f"useful_{selected_student}_{row['topic']}_{idx}"):
                    save_feedback(selected_student, row['topic'], rec_text, "Useful")
                    st.success("Thank you for your feedback!")
                if col_fb2.button("👎 Not Useful", key=f"not_useful_{selected_student}_{row['topic']}_{idx}"):
                    save_feedback(selected_student, row['topic'], rec_text, "Not Useful")
                    st.info("Feedback recorded. We will improve our recommendations.")

elif role == "Teacher / Admin Portal":
    st.header("Teacher & Academic Administrator Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Enrolled Students", engine.df['student_id'].nunique())
    with col2:
        st.metric("Average Class Attendance", f"{engine.df['attendance_pct'].mean():.1f}%")
    
    st.markdown("### Class-Wide Subject Performance Distribution")
    fig_class = px.box(engine.df, x='subject', y='exam_mark', color='subject', title="Exam Mark Distribution across Subjects")
    st.plotly_chart(fig_class, use_container_width=True)
    
    st.markdown("### Students Needing Immediate Support")
    all_weak = engine.df[
        (engine.df['exam_mark'] < 60) | 
        (engine.df['quiz_score'] < 60) | 
        (engine.df['attendance_pct'] < 75.0)
    ][['student_id', 'subject', 'topic', 'exam_mark', 'attendance_pct']]
    
    st.dataframe(all_weak, use_container_width=True)
    
    st.markdown("### Student Feedback Analytics")
    feedback_df = get_all_feedback()
    if not feedback_df.empty:
        st.dataframe(feedback_df, use_container_width=True)
    else:
        st.info("No recommendation feedback collected yet.")