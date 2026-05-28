from google import genai
from google.genai import types

# 1. Initialize the client with your new API key
client = genai.Client(api_key="AIzaSyBPRkJ8ArYT6BuReeiPg3yI5r6xVOnBI28")


def check_for_fake_news(text):
    print(f"Analyzing: '{text}'...\n")

    # 2. Tell Gemini exactly how to behave using a system instruction
    config = types.GenerateContentConfig(
        system_instruction="You are an expert fact-checker. Analyze the provided text. Determine if it is likely real news, fake news, or satire. Provide a brief explanation of your reasoning and a confidence percentage."
    )

    try:
        # 3. Send the text to the model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=text,
            config=config
        )

        print("--- Gemini Classification Results ---")
        print(response.text)
        print("-------------------------------------")

    except Exception as e:
        print("Whoops, something went wrong:", e)


# Test it out!
test_text = "NASA has officially confirmed that the moon is made entirely of expired green cheese, according to a deleted tweet."
check_for_fake_news(test_text)
