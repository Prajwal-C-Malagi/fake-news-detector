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

                # UPDATED INSTRUCTION: Formatted safely to avoid Syntax Errors
                instruction = (
                    f"You are an expert fact-checker analyzing text. Today's real-world date is {today}. "
                    "Search the web to verify the claim. You MUST reply ONLY with a raw JSON object. "
                    "Do not wrap your answer in markdown code blocks. Use exactly this structure: "
                    '{"classification": "Real/Fake/Satire", "confidence_score": 95, "reasoning": "1-sentence reason", "search_query": "A 3 to 5 word query to find visual proof of the actual truth"}'
                )

                config = types.GenerateContentConfig(
                    system_instruction=instruction,
                    temperature=0.1,
                    tools=[{"google_search": {}}]
                )

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=text_input,
                    config=config
                )

                clean_text = response.text.strip(
                    "` \n\r").replace("json", "", 1).strip()
                result = json.loads(clean_text)

                # 3. Display the text results
                st.divider()

                classification = result['classification'].upper()
                if 'FAKE' in classification:
                    st.error(f"🚨 Classification: **{classification}**")
                elif 'SATIRE' in classification:
                    st.warning(f"🎭 Classification: **{classification}**")
                else:
                    st.success(f"✅ Classification: **{classification}**")

                st.metric(label="AI Confidence Score",
                          value=f"{result['confidence_score']}%")
                st.markdown(f"**Reasoning:** {result['reasoning']}")

                # 4. FETCH AND DISPLAY VISUAL PROOF
                st.markdown("### 📸 Visual Evidence")
                with st.spinner("Pulling photographic proof..."):
                    try:
                        # Use the AI's search query to find the top image on the web
                        search_results = DDGS().images(
                            result['search_query'], max_results=1)
                        if search_results:
                            image_url = search_results[0]['image']
                            # Display the image beautifully in Streamlit
                            st.image(
                                image_url, caption=f"Web Result for: '{result['search_query']}'", use_container_width=True)
                        else:
                            st.info(
                                "Could not find a relevant image for this claim.")
                    except Exception as img_e:
                        st.warning(
                            f"Visual evidence engine is currently busy. (Hidden Error: {img_e})")

            except Exception as e:
                st.error(f"An error occurred parsing the response: {e}")
                if 'response' in locals():
                    st.text_area("Raw AI Response:",
                                 value=response.text, height=100)
    else:
        st.warning("Please enter some text first!")
