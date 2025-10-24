import datetime
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("LLM_Key"))

model = genai.GenerativeModel('gemini-2.0-flash')

def send_message_to_llm(message_for_llm):
    response = model.generate_content(message_for_llm)

    # Get current date and time for the filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the filename
    filename = os.path.join("logs", f"response_{timestamp}.txt")

    # Write to the generated file
    with open(filename, 'w') as f:
        f.write(message_for_llm, response.text)
