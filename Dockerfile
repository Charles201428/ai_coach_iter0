# Use an official lightweight Python image
FROM python:3.10-slim

# Prevent Python from buffering stdout/stderr (streamlit logs flush immediately)
ENV PYTHONUNBUFFERED=1

# Streamlit settings: run headless on port 8501, listen on all interfaces
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Working directory inside the container
WORKDIR /app

# Copy and install Python dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose Streamlit’s default port
EXPOSE 8080

# At runtime, supply your HF_API_TOKEN via env var: 
#   docker run -e HF_API_TOKEN=hf_xxx -p 8501:8501 ai-coach
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
