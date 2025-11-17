import datetime
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("CHAT_API_KEY"))

genai.configure(api_key=os.getenv("LLM_Gemini_Key"))
model = genai.GenerativeModel('gemini-2.0-flash')

hook_message = "You are an expert database analyst, and you specialize in database breaches." \
    "Your job is to solve problems about database breaches in a concise manner."

def send_message_to_openai(message):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "system", "content": hook_message},
        {"role": "user", "content": message}])

    # Extract the response text
    reply = response.choices[0].message.content

    #get time where the llm response was resived
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the file and the folder if not existing
    script_dir = Path(__file__).parent
    log_folder = script_dir / "logs_openai"
    os.makedirs(log_folder, exist_ok=True)
    filename = os.path.join(log_folder, f"response_{timestamp}.txt")

    # Write both the message and response to the log file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("User message:\n" + message + "\n\n")
        f.write("LLM response:\n" + reply)

    return reply

def send_message_to_gemini(message):
    messages = [
        {"role": "assistant", "parts": [hook_message]},
        {"role": "user", "parts": [message]}
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
        f.write(f"Message:\n{message}\n\nResponse:\n{response}")
    return response