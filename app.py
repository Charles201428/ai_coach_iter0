# app.py
import streamlit as st
import os
from model import generate_coach_response
from data_store import load_user_history, save_user_history

# --- Helper: Ensure an event loop exists (optional) ---
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# --- Login Section ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("Login to AI Coach")
    
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        # Dummy login: in a real app use a proper user system
        if username_input == "user" and password_input == "password":
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            # Load user's conversation history, if any
            st.session_state["history"] = load_user_history(username_input)
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Please try again.")
    st.stop()  # Prevent further execution if not logged in.

# --- Main App Interface (after login) ---
st.title("AI Coach for Capstone Projects")
st.write("Ask any question about the project solution to get expert guidance.")

# Load the pre-provided knowledge (solution details)
knowledge_file = "solution_knowledge.txt"
if not os.path.exists(knowledge_file):
    st.error("Missing solution_knowledge.txt file.")
    st.stop()
with open(knowledge_file, "r", encoding="utf-8") as f:
    knowledge_text = f.read()

# Display conversation history
if "history" not in st.session_state:
    st.session_state["history"] = []
    
st.subheader("Conversation History")
if st.session_state["history"]:
    for turn in st.session_state["history"]:
        st.write(f"**User:** {turn['user']}")
        st.write(f"**Coach:** {turn['coach']}")
else:
    st.write("No conversation history yet.")

# Input form for new query
st.subheader("Ask a Question")
new_query = st.text_input("Your question:", key="query_input")

if st.button("Submit Question"):
    if new_query.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Generating response..."):
            # You could also incorporate previous conversation history as additional context if desired.
            response = generate_coach_response(new_query, knowledge_text)
        # Append to session history
        new_turn = {"user": new_query, "coach": response}
        st.session_state["history"].append(new_turn)
        # Save updated history to persistent storage
        save_user_history(st.session_state["username"], st.session_state["history"])
        st.experimental_rerun()  # Refresh the page to display the updated history.
