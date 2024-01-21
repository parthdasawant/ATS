import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()  # load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_repsonse(input, top_k, top_p):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input, generation_config=genai.types.GenerationConfig(
        temperature=0,
        top_k=top_k,
        top_p=top_p))
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template


input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field,software engineering and {jr}. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide best assistance for improving the resumes. Assign the percentage Matching based on Jd, job roles and the missing keywords with high accuracy
resume:{text}
description:{jd}
job role:{jr}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""
# input_prompt = """
# As a seasoned ATS (Application Tracking System) with expertise in the tech field, specializing in based on given job position/role, your task is to evaluate a resume based on a given job description.

# Please provide the following inputs:

# 1. resume: {text}
# 2. Job Position/Role: {jr}
# 3. Job Description (JD): {jd}

# Ensure the job market is highly competitive, and your evaluation should offer the best assistance for resume improvement. Assign a percentage match based on the JD, identify missing keywords with high accuracy, and generate a profile summary.

# Response Structure:
# {
#   "JD Match": "%",
#   "MissingKeywords": [],
#   "Profile Summary": ""
# }

# """
# streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
jr = st.text_area("Job Roles")
uploaded_file = st.file_uploader(
    "Upload Your Resume", type="pdf", help="Please uplaod the pdf")
top_k = st.slider(label="top_k", min_value=1, max_value=5, value=3)
top_p = st.slider(label="top_p", min_value=0.0,
                  max_value=1.0, value=0.01, step=0.01)
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_repsonse(input_prompt, top_k, top_p)
        st.subheader(response)
