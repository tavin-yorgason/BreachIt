import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

genai.configure(api_key=os.getenv("LLM_Gemini_Key"))

model = genai.GenerativeModel('gemini-2.0-flash')

def send_message_to_llm(message_for_llm):
    messages = [
        {"role": "system", "parts": ["You are an LLM deciding if a SQL database has been breached."]},
        {"role": "user", "parts": [message_for_llm]}
    ]

    response = model.generate_content(messages).candidates[0].content.parts[0].text

    # Get current date and time for the filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the file
    script_dir = Path(__file__).parent  
    log_folder = script_dir / "logs_gemini"
    os.makedirs(log_folder, exist_ok=True)
    filename = os.path.join(log_folder, f"response_{timestamp}.txt")

    # Write to the generated file
    with open(filename, 'w') as f:
        f.write(f"Message:\n{message_for_llm}\n\nResponse:\n{response}")

    return response