# model.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN not found in environment. Please set it in your .env file.")

# Define endpoints and headers for API calls
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# Endpoint for the main coaching response
COACH_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
# Endpoint for summarization using facebook/bart-large-cnn
SUMMARIZATION_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

def query(api_url, payload):
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def summarize_text(text, max_length=200):
    """
    Summarize the provided text using the HF Inference API with facebook/bart-large-cnn.
    If the API call fails (e.g., 503 error), fall back to simple truncation.
    
    Parameters:
      text (str): The text to summarize.
      max_length (int): The maximum length of the summary.
      
    Returns:
      str: The summarized (or truncated) text.
    """
    try:
        payload = {
            "inputs": text,
            "parameters": {"max_length": max_length, "min_length": 50, "do_sample": False}
        }
        result = query(SUMMARIZATION_API_URL, payload)
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"].strip()
        else:
            # Fallback: if API returns an unexpected format, truncate text.
            return text[:max_length] + "..."
    except requests.exceptions.HTTPError as e:
        # Log the error and return a truncated version of the text.
        print(f"Summarization API error: {e}. Falling back to truncation.")
        return text[:max_length] + "..."

def generate_coach_response(query_text, knowledge_text, resume_text=""):
    """
    Generates an AI coach response by integrating:
      - The coaching role for online assessment preparation.
      - A sample solution reference (predefined knowledge), summarized if needed.
      - Optionally, the user's resume details, summarized if needed.
      
    Parameters:
      query_text (str): The user's question.
      knowledge_text (str): The full sample solution reference text.
      resume_text (str): The user's resume text (optional).
      
    Returns:
      str: The AI coach's response.
    """
    KNOWLEDGE_THRESHOLD = 2000  # threshold for knowledge_text
    RESUME_THRESHOLD = 1500     # threshold for resume_text

    # Summarize knowledge_text if it's too long
    if len(knowledge_text) > KNOWLEDGE_THRESHOLD:
        summarized_knowledge = summarize_text(knowledge_text, max_length=200)
    else:
        summarized_knowledge = knowledge_text

    # Summarize resume_text if provided and too long
    summarized_resume = ""
    if resume_text:
        if len(resume_text) > RESUME_THRESHOLD:
            summarized_resume = summarize_text(resume_text, max_length=150)
        else:
            summarized_resume = resume_text

    # Build the resume section if available
    resume_section = f"User's Resume Details (extracted):\n{summarized_resume}\n\n" if summarized_resume else ""

    # Build the complete prompt for the coach
    prompt = f"""
You are an AI coach specializing in helping candidates prepare for online assessments.
Your role is to provide guidance, strategies, and clarifications on solving various online assessment tasks.
While you have access to a sample solution reference for one specific task—the AI-powered cold outreach tool—your coaching should be broadly applicable.
Use the information below to inform your answer.

{resume_section}
Sample Solution Reference (condensed):
{summarized_knowledge}

A user now asks:
{query_text}

Provide a clear, detailed, and helpful answer tailored for a candidate preparing for an online assessment.
Answer:"""
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "do_sample": True
        }
    }
    
    result = query(COACH_API_URL, payload)
    
    if isinstance(result, list) and "generated_text" in result[0]:
        generated_text = result[0]["generated_text"].strip()
        if "Answer:" in generated_text:
            response = generated_text.split("Answer:", 1)[1].strip()
        else:
            response = generated_text
        return response
    else:
        return str(result)
