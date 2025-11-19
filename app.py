# app_safe_start.py  -- paste contents into your app.py (replace existing)
import streamlit as st
import traceback, sys, time

st.set_page_config(page_title="JD Analyzer (Safe start)", layout="wide")

st.title("JD Analyzer · Skill Comparator · CV Enhancer")
st.caption("Safe startup mode — click the button below to load heavy models. Errors will be shown here.")

st.markdown("""
**Why this mode?**  
Streamlit sometimes shows a blank page if heavy model imports block startup or crash. Click **Load models & start** to load models safely and see any error messages.
""")

load_btn = st.button("Load models & start (may take 10–60s)")

# show a quick health check area (always visible)
st.markdown("### Health check")
st.write("Python version:", sys.version.splitlines()[0])
st.write("Streamlit version:", st.__version__)
st.write("Time:", time.strftime("%Y-%m-%d %H:%M:%S"))

if load_btn:
    with st.spinner("Loading models (will be cached). Please wait..."):
        try:
            # Lazy imports and model loads inside try/except
            import re, io, json
            from sentence_transformers import SentenceTransformer, util
            import spacy
            import pdfplumber
            from docx import Document
            from fuzzywuzzy import fuzz
            import pandas as pd

            # Load spaCy model safely
            try:
                nlp = spacy.load("en_core_web_sm")
            except Exception as e_spacy:
                st.error("spaCy model load error. You must include `python -m spacy download en_core_web_sm` in your deploy step or vendor the model.")
                st.exception(e_spacy)
                st.stop()

            # Load embedding model (smaller model)
            try:
                EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e_model:
                st.error("Embedding model download/load failed. See details below.")
                st.exception(e_model)
                st.stop()

            st.success("Models loaded successfully!")
            # Optionally redirect to the main app logic or display a button to continue
            st.write("Now you can run the full app logic. For production, move heavy model loads into a cached function and ensure dependencies are in requirements.txt.")
            # You can now import or call the rest of your app functions here or navigate user to next step.

        except Exception as e:
            st.error("Unexpected error while loading models.")
            st.text(traceback.format_exc())
            st.stop()
