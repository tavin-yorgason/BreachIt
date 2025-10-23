from llm_communication import send_message_to_llm

def build_llm_message(db_setup, db_query, db_response):
    return (
        f"Gemini for this problem decide if the Database was breached or not here is the database setup: {db_setup}"
        f" Now you have the general idea of the database setup now follows the SQL query: {db_query}"
        f" After executing the SQL query that was the response: {db_response}"
        " So now did our database get breached or not?"
    )

def coordinate_communication_llm_database(db_setup, db_query, db_response):
    message_llm = build_llm_message(db_setup, db_query, db_response)
    return send_message_to_llm(message_llm)
