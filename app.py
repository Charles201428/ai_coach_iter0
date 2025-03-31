# app.py
import streamlit as st
from model import generate_coach_response

# --- Load Pre-Provided Knowledge ---
try:
    with open("solution_knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_text = f.read()
except FileNotFoundError:
    st.error("The solution knowledge file is missing. Please add 'solution_knowledge.txt' to your project folder.")
    st.stop()

# --- Streamlit App Interface ---
st.title("AI Coach for Capstone Projects")
st.write("Ask any question about the project solution and get expert guidance.")

# User input: A text box for questions
query = st.text_input("Enter your question here:")

if st.button("Get Coach Response"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating response..."):
            response = generate_coach_response(query, knowledge_text)
        st.subheader("Coach Response:")
        st.write(response)
