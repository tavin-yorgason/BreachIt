import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("LLM_OpenAI_Key"))

def send_message_to_llm(message_for_llm):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "system", "content": "You are an LLM deciding if a SQL database has been breached."},
        {"role": "user", "content": message_for_llm}])

    # Extract the response text
    reply = response.choices[0].message.content

    #get time where the llm response was resived
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the file and the folder if not existing
    script_dir = Path(__file__).parent  
    log_folder = script_dir / "logs_Openai"
    os.makedirs(log_folder, exist_ok=True)
    filename = os.path.join(log_folder, f"response_{timestamp}.txt")

    # Write both the message and response to the log file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("User message:\n" + message_for_llm + "\n\n")
        f.write("LLM response:\n" + reply)

    return reply

    
