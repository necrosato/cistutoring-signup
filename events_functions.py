from datetime import datetime, timedelta

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

def datetime_range_strings(year, month, day, start_hour, end_hour, num_days, weekends=True):
    first_date = datetime(year, month, day, start_hour)
    dts = []
    for i in range(num_days):
        start_date = first_date + timedelta(days=i)
        end_date = start_date + timedelta(hours=(end_hour - start_hour))
        if (weekends == False and (start_date.weekday() > 4)):
            continue;

        dts.append([dt.strftime('%Y-%m-%d %H:%M:%S') for dt in 
               datetime_range(start_date, end_date, 
               timedelta(minutes=30))])
    return dts

def populate_events_table(dbcursor, year, month, day, start_hour, end_hour, num_days, weekends=True):
    dts = datetime_range_strings(year, month, day, start_hour, end_hour, num_days, weekends)

    check_query = "SELECT id FROM events WHERE start=?"
    query = "INSERT INTO events (start) VALUES (?)"
    for dtl in dts:
        for dt in dtl:
            dbcursor.execute(check_query, (dt,))
            if (len(dbcursor.fetchall() == 0)):
                dbcursor.execute(query, (dt,))

    end_query = "UPDATE events SET end = DATE_ADD(start, INTERVAL 30 minute)"
    dbcursor.execute(end_query)

def is_reserved(dbcursor, dt, uid):
    check_query = "SELECT id FROM events WHERE start=%s AND uid=%s"
    dbcursor.execute(check_query, (dt,uid,))
    rows = dbcursor.fetchall()
    if (len(rows) == 1):
        return True
    else:
        return False
    
#
## these are the settings for Winter 2018
#year = 2018
#month = 1
#day = 8
#start_hour = 8
#end_hour = 20
#num_days = (10*7) #10 weeks in a term
#weekends = False
#dts = datetime_range_strings(year, month, day, start_hour, end_hour, num_days, weekends)
#for dtl in dts:
#    for dt in dtl:
#        print(dt)
#
#
