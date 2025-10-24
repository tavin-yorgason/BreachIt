import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

genai.configure()

model = genai.GenerativeModel('gemini-2.0-flash')

def send_message_to_llm(message_for_llm):
    print(f"about to send \"{message_for_llm}\" to llm")
    response = model.generate_content(message_for_llm).candidates[0].content.parts[0].text
    print(f"response: {response}")

    # Get current date and time for the filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the file
    script_dir = Path(__file__).parent  
    log_folder = script_dir / "logs"
    os.makedirs(log_folder, exist_ok=True)
    filename = os.path.join(log_folder, f"response_{timestamp}.txt")

    # Write to the generated file
    with open(filename, 'w') as f:
        f.write(f"Message:\n{message_for_llm}\n\nResponse:\n{response}")

    return response
