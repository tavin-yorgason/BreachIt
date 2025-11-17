import database
from database import databases
from pathlib import Path

#try:
database.execute_query(
    "DROP TABLE gemini_attacks_gemini, gemini_attacks_openai, " +
    "openai_attacks_gemini, openai_attacks_openai",
    databases.DB_ATTACKS
)
#except:
#    print(
#        "Error dropping tables. This probably means one or more tables were already gone."
#    )

database.execute_queries(
    Path("db_attacks_tables.sql").read_text(),
    databases.DB_ATTACKS
)