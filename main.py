import streamlit as st
import PyPDF2
import io
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


st.set_page_config(page_title="Resume Critiquer", page_icon="📃", layout="centered")
st.title("AI Resume Critiquer 📃")
st.markdown("Upload your resume in PDF format and get feedback on its content.")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF of TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're taregtting (optional)")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content...")
            st.stop()

        # Prepare the prompt for the AI model
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations.""" 

        # Initialize the Anthropic client
        client = Anthropic(api_key=ANTHROPIC_API_KEY)

        # Call the Anthropic API to analyze the resume (directly invoking the LLM)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000, # Required for Anthropic messages API
            system="You are an expert resume reviewer with years of experience in HR and recruitment.",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        # Display the analysis results
        st.markdown("### Analysis Results")
        st.markdown(response.content[0].text)

    except Exception as e:
        st.error(f"An error occured: {str(e)}")