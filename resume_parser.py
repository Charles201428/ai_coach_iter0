# resume_parser.py
import io
from pdfminer.high_level import extract_text
import docx

def parse_resume(file):
    """
    Extracts text content from a resume file.
    Supports PDF and DOCX formats.

    Parameters:
        file (UploadedFile): A file-like object (e.g., from Streamlit's file uploader)
                             having a filename attribute.

    Returns:
        dict: A dictionary containing a "full_text" key with the extracted text, or an error message.
    """
    resume_data = {}
    # Determine file type based on file extension
    file_type = file.name.split('.')[-1].lower()

    if file_type == 'pdf':
        try:
            # For PDF files, extract text using pdfminer.
            # The file is expected to be a file-like object (e.g., BytesIO).
            text = extract_text(file)
        except Exception as e:
            text = f"Error extracting PDF text: {str(e)}"
        resume_data["full_text"] = text

    elif file_type == 'docx':
        try:
            # For DOCX files, use python-docx to read document content.
            doc = docx.Document(file)
            # Join all paragraphs into a single string separated by newlines.
            full_text = [para.text for para in doc.paragraphs]
            text = "\n".join(full_text)
        except Exception as e:
            text = f"Error extracting DOCX text: {str(e)}"
        resume_data["full_text"] = text

    else:
        resume_data["full_text"] = "Unsupported file type."

    return resume_data
