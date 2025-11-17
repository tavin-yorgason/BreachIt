from database import execute_query

def check_query(user_query: str):
    try:
        result = execute_query(user_query)

        # SELECT: list of dicts
        if isinstance(result, list):
            if not result:
                return {
                    "ok": True,
                }

            columns = list(result[0].keys())
            rows = [list(r.values()) for r in result]

            return {
                "ok": True,
            }

        # Non-select (UPDATE/INSERT/DELETE)
        if isinstance(result, str):
            return {
                "ok": True,
            }

        return {
            "ok": False,
        }

    except Exception as e:
        return {
            "ok": False,
        }

