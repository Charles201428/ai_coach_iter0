import streamlit as st
from model import generate_coach_response

# For resume parsing, import your parser module (assuming resume_parser.py exists)
import resume_parser

# -------------------------------
# 1) Handle Login (Simple Mock)
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

def login(username, password):
    valid_users = {"user1": "password1", "user2": "password2"}
    return valid_users.get(username) == password

if not st.session_state["logged_in"]:
    st.title("Login to AI Coach")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials. Please try again.")
    st.stop()

# -------------------------------
# 2) Sidebar - Resume Uploader
# -------------------------------
st.sidebar.header("User Profile")
resume_file = st.sidebar.file_uploader("Upload/Update your resume (PDF format)", type=["pdf"])
if resume_file is not None:
    try:
        resume_data = resume_parser.parse_resume(resume_file)
        st.session_state["resume_text"] = resume_data.get("full_text", "")
        st.sidebar.success("Resume uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error parsing resume: {e}")
else:
    # If no resume is uploaded yet, ensure there is an empty placeholder
    if "resume_text" not in st.session_state:
        st.session_state["resume_text"] = ""

# -------------------------------
# 3) Initialize Chat Session
# -------------------------------
st.title("AI Coach for Online Assessment Preparation")

# Load sample solution knowledge from file
try:
    with open("solution_knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_text = f.read()
except FileNotFoundError:
    st.error("The solution knowledge file is missing. Please add 'solution_knowledge.txt' to your project folder.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Hello, I'm your AI Coach! I can help you prepare for online assessments. "
                "Feel free to ask me about the sample solution (AI-powered cold outreach), your resume, or any general questions you may have!"
            )
        }
    ]

# 4) Display Existing Conversation
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5) Chat Input Section at the Bottom
user_input = st.chat_input("Type your question here...")

if user_input:
    # Append user's message to conversation history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate the coach's reply, including the resume if available
    if user_input.lower() in ["hello", "hi", "hey"]:
        coach_reply = "Hello! How can I help you with your online assessment preparations today?"
    else:
        resume_text = st.session_state.get("resume_text", "")
        coach_reply = generate_coach_response(user_input, knowledge_text, resume_text)

    with st.chat_message("assistant"):
        st.write(coach_reply)
    st.session_state["messages"].append({"role": "assistant", "content": coach_reply})
