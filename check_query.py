from database import execute_query_redacted


# ---------- Unsafe words ----------

# Any query containing one of these (after lowercasing) is automatically unsafe.
BAD_SQL_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "replace",
    "drop",
    "alter",
    "truncate",
}


# ---------- Normalization helper ----------

def normalize_query(query: str) -> str:
    """
    Strip extra whitespace, remove trailing semicolon, and lowercase the query
    so text checks are consistent.
    """
    q = query.strip()
    if q.endswith(";"):
        q = q[:-1]

    # Collapse all whitespace runs (spaces, newlines, tabs) to a single space
    q = " ".join(q.split())
    return q.lower()


# ---------- Allowed columns (across all tables) ----------

# This should be the union of all columns that are allowed to appear
# in any SELECT result.
ALLOWED_COLUMNS = {
    # items
    "item_id", "price", "name", "description",
    # users
    "username", "email", "birthdate",
    # transactions
    "transaction_id", "time",
    # transaction_items
    "quantity",
    # cart_items reuses username, item_id, quantity
}


def is_query_safe(user_query: str) -> bool:
    """
    Return True if the query is considered safe, False otherwise.

    Policy:
    - Only SELECT queries are allowed.
    - No INSERT/UPDATE/DELETE/DROP/etc.
    - Any query that mentions the users table must explicitly filter
      to username='default'.
    - The query is executed in a redacted world where only default-user
      data exists (via TEMPORARY TABLEs).
    - Every column of every returned row must be in ALLOWED_COLUMNS,
      and any username value must be exactly 'default'.
    """

    normalized = normalize_query(user_query)

    # 1. Block obviously dangerous commands
    for kw in BAD_SQL_KEYWORDS:
        if kw in normalized:
            return False

    # 2. Require a SELECT query
    if not normalized.startswith("select"):
        return False

    # 3. If the query touches the users table, require username='default'
    #    somewhere in the WHERE clause (simple but effective guard).
    if " from users" in normalized or " join users" in normalized:
        if (
            " where username = 'default'" not in normalized
            and " where username='default'" not in normalized
        ):
            return False

    # 4. Execute against the redacted TEMPORARY TABLE world
    try:
        result = execute_query_redacted(user_query)
    except Exception:
        # Bad syntax, runtime error, etc. -> treat as unsafe
        return False

    # 5. We expect SELECT results to be a list of dict rows
    if not isinstance(result, list):
        return False

    # Empty result set: nothing leaked
    if not result:
        return True

    # 6. Brute-force scan over every row and every column
    for row in result:
        if not isinstance(row, dict):
            return False

        for col_name, value in row.items():
            # Column name must be in the approved set
            if col_name not in ALLOWED_COLUMNS:
                return False

            # Any username value must be exactly 'default'
            if col_name == "username" and value != "default":
                return False

    # If we reach here, nothing violated the rules
    return True