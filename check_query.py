from database import execute_query

def check_query(user_query: str):
    try:
        result = execute_query(user_query)

        # SELECT: list of dicts
        if isinstance(result, list):
            if not result:
                return {
                    "ok": True,
                    "columns": [],
                    "rows": [],
                    "error": None
                }

            columns = list(result[0].keys())
            rows = [list(r.values()) for r in result]

            return {
                "ok": True,
                "columns": columns,
                "rows": rows,
                "error": None
            }

        # Non-select (UPDATE/INSERT/DELETE)
        if isinstance(result, str):
            return {
                "ok": True,
                "columns": ["message"],
                "rows": [[result]],
                "error": None
            }

        return {
            "ok": False,
            "columns": [],
            "rows": [],
            "error": "Unexpected data type returned from database"
        }

    except Exception as e:
        return {
            "ok": False,
            "columns": [],
            "rows": [],
            "error": str(e)
        }

