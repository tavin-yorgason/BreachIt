from build_llm_message import build_defender_message, build_attacker_message
from llm_communication import send_message_to_openai, send_message_to_gemini
import database
import re
import argparse

def main():
    attacker, defender, count = parse_arguments()

    print(f"Attacker: {attacker}\n"
          f"Defender: {defender}\n"
          f"Attack count: {count}\n")

    # Set attacker and defender message functions
    message_attacker, message_defender = get_message_functions(attacker, defender)

    # Attack the database
    attacker_message = build_attacker_message()
    for _ in range(count):
        attacker_response = message_attacker(attacker_message)
        query = extract_query(attacker_response)

        query_result = ""
        try:
            query_result = database.execute_query(query)
        except Exception as e:
            query_result = f"Error: {e}"

        defender_response = message_defender(build_defender_message(query, query_result))

        does_conclude_yes(defender_response)

def does_conclude_yes(message):
    message_lower = message.lower()
    message_contains_yes = "yes" in message_lower
    message_contains_no = "no" in message_lower

    if message_lower.startswith("no"):
        return False
    elif message_lower.startswith("yes"):
        return True
    elif not (message_contains_no and message_contains_yes) \
        or (message_contains_no and message_contains_yes):
        raise Exception("Unable to find distinct response.")
    elif message_contains_yes:
        return True
    elif message_contains_no:
        return False

def extract_query(message):
    # The ? makes it find the smallest possible match in case there are multiple
    # queries.
    match = re.search(r"```sql(.*?)```", message, flags=re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        print("Regex failed, message may not have a query.")
        return message

def get_message_functions(attacker, defender):
    message_attacker = None
    message_defender = None

    if attacker == "gemini":
        message_attacker = send_message_to_gemini
    else:
        message_attacker = send_message_to_openai

    if defender == "gemini":
        message_defender = send_message_to_gemini
    else:
        message_defender = send_message_to_openai

    return message_attacker, message_defender

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--attacker")
    parser.add_argument("--defender")
    parser.add_argument("--count", type=int, required=True)

    args = parser.parse_args()

    if args.count <= 0:
        parser.error("Count cannot be less than 1.")

    if not args.attacker and not args.defender:
        parser.error("Please input an attacker and/or defender.\n"
            "If you only input one, the other will be the other LLM.")

    attacker = ""
    defender = ""

    if args.attacker and args.defender:
        attacker = args.attacker
        defender = args.defender
    elif args.defender:
        defender = args.defender
        attacker = get_other_llm(defender)
    else:
        attacker = args.attacker
        defender = get_other_llm(attacker)

    check_llm(attacker)
    check_llm(defender)

    return attacker, defender, args.count

def get_other_llm(llm):
    if llm == "gemini":
        return "openai"
    else:
        return "gemini"

def check_llm(llm):
    if llm != "gemini" and llm != "openai":
        print(f"'{llm}' is an invalid LLM. Valid LLMs are: 'gemini', 'openai'")
        exit(1)

if __name__ == '__main__':
    main()
