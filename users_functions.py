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

def user_change_password(dbcursor, user, password):
    query = "UPDATE users SET password = PASSWORD(%s) WHERE email = %s"
    dbcursor.execute(query, (password,user,))

def user_create(dbcursor, name, email, password, phone=None):
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, PASSWORD(%s))"
    query_phone = "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, PASSWORD(%s))"
    dbcursor.execute(query, (name, email, password,)) if phone == None else dbcursor.execute(query_phone, (name, email, phone, password))

def user_delete(dbcursor, name, email, password):
    query = "DELETE FROM users WHERE name = %s AND email = %s AND password = PASSWORD(%s)"
    dbcursor.execute(query, (name, email, password,))

