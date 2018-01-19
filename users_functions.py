def valid_user(dbcursor, user):
    query = "SELECT email FROM users WHERE email = %s"
    dbcursor.execute(query, (user,))
    rows = dbcursor.fetchall()
    if (len(rows) == 1):
        return True
    else:
        return False

def valid_password(dbcursor, user, password):
    query = "SELECT password FROM users WHERE password = PASSWORD(%s) and email = %s"
    dbcursor.execute(query, (password,user,))
    rows = dbcursor.fetchall()
    if (len(rows) == 1):
        return True
    else:
        return False
