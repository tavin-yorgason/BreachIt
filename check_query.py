from database import execute_query

#---------- Unsafe Words ---------

#Bad SQL = Not Safe, auto set as false  
Bad_SQL_keywords = {
    "insert",
    "update",
    "delete",
    "replace",
    "drop",
    "alter",
    "truncate",
}

#---------- Remove input differneces ----------

def normalize_query(query: str) -> str:
    q = query.strip()
    if q.endswith(";"):
        q = q[:-1]

    q = " ".join(q.split())
    return q.lower()

#---------- Rules ----------

Allowed_Collumns = {
    "item_id", "price", "name", "description",
    "username", "email", "birthdate",
    "transaction_id", "time", "quantity",   
}

def is_query_safe(user_query : str) -> bool:
#Only safe if they fall within allowed collumn names and username is set as default

    normalized = normalize_query(user_query)

    #Bad SQL check 
    for kw in Bad_SQL_keywords:
        if kw in normalized:
            return False
        
    #If it starts with anything but "select"
    if not normalized.startswith("select"):
        return False
    
    if "from users" in normalized or " join users" in normalized:
        if 'where username = "default"' not in normalized and \
        "where username='default'" not in normalized:
            return False
    
    #Run the Query 
    try:
        result = execute_query(user_query)
    except Exception:
        return False #does not run
    
    if not isinstance(result, list): 
        return False #Somehow let Bad SQL through, just to double check 
    
    for row in result: 
        for col_name, value in row.items():
            if col_name not in Allowed_Collumns:
                return False
            
        if col_name == "username" and value != "default":
            return False
       
    return True 