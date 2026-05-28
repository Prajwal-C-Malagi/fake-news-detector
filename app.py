import streamlit as st
from google import genai
from google.genai import types
import json
import datetime
from duckduckgo_search import DDGS

# 1. Initialize client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Design the Streamlit UI
st.set_page_config(page_title="AI Fact Checker", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ AI Fake News Detector")
st.markdown(
    "Paste a news headline, article snippet, or social media post below to verify its authenticity.")

text_input = st.text_area("Content to analyze:",
                          height=150, placeholder="Type or paste text here...")

# Trigger the API
if st.button("Check Authenticity"):
    if text_input:
        with st.spinner("Searching the web and verifying facts..."):
            try:
                today = datetime.date.today().strftime("%B %d, %Y")

                # UPDATED INSTRUCTION: We added "search_query" to the JSON structure
                instruction = (
                    f"You are an expert fact-checker analyzing text. Today's real-world date is {today}. "
                    "Search the web to verify the claim. You MUST reply ONLY with a raw JSON object. "
                    "Do not wrap your answer in markdown code blocks like
