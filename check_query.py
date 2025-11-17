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
    
    #Run the Query 
    try:
        result = execute_query(user_query)
    except Exception:
        return False #does not run
    
    if not isinstance(result, list): 
        return False #Somehow let Bad SQL through, just to double check 
    
    if not result:
        return True 
    
    columns = set(result[0].keys()) #Data is returned, needs to be checked 

    if not columns.issubset(Allowed_Collumns): #If data is not an allowed collum, false 
        return False

    #If username is returned, must be "default"
    if "username" in columns:
        for row in result:
            if row.get("username") != "default":
                return False
            
    return True 