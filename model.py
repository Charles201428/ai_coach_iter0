# model.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- Configuration ---
# Replace with the exact model name of your chosen free LLaMA model.
# For this toy iteration, we'll use a small model variant for faster inference.
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Ensure you have access to this model on Hugging Face

# --- Load Tokenizer and Model ---
# If you have a GPU available, device_map="auto" will place model parts on GPU
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

def generate_coach_response(query, knowledge_text):
    """
    Generate an AI coach response by combining the pre-provided knowledge with the user's query.
    
    Parameters:
      query (str): The user's question.
      knowledge_text (str): The text containing your solution details.
      
    Returns:
      response (str): The generated answer from the AI coach.
    """
    # Construct a detailed prompt that gives the model context about your solution
    prompt = f"""
You are an expert AI coach who is extremely knowledgeable about the following project solution:
{knowledge_text}

A user now asks a question about the project:
{query}

Please provide a clear, detailed, and helpful answer.
    """
    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    # Generate a response with some creativity (temperature=0.7) and up to 200 new tokens
    output_ids = model.generate(**inputs, max_new_tokens=200, temperature=0.7, do_sample=True)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response.strip()
