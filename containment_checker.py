from database import execute_query
from pathlib import Path

safe_queries_path = Path(__file__).parent / "safe_queries.sql"

def load_queries_from_file(path):
    queries = []
    with open(path, "r") as f:
        buffer = ""
        for line in f:
            line = line.strip()
            if not line:
                continue

            buffer += " " + line

            # End of SQL statement
            if buffer.strip().endswith(";"):
                queries.append(buffer.strip())
                buffer = ""

    return queries

def build_allowed_cells_dicts(safe_queries, execute_query):
    allowed = set()

    for q in safe_queries:
        results = execute_query(q)

        for row in results:
            for value in row.values():
                allowed.add(value)

    return allowed


def detect_leak_cells_dicts(attack_results, allowed_cells):
    leaked = []

    for row in attack_results:
        for value in row.values():
            if value not in allowed_cells:
                leaked.append({"row": row, "leaked_value": value})
                break

    return leaked


def is_query_breaching(attack_query):
    safe_queries = load_queries_from_file(safe_queries_path)

    allowed_results = build_allowed_cells_dicts(
        safe_queries,
        execute_query
    )

    attack_results = execute_query(attack_query)

    leaks = detect_leak_cells_dicts(attack_results, allowed_results)

    if leaks:
        print("LEAK DETECTED!")
        return True
    else:
        print("No leak.")
        return False
