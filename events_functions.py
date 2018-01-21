from datetime import datetime, timedelta

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

def datetime_range_strings(year, month, day, start_hour, start_minute, end_hour, end_minute, num_days, weekends=True, weekly=False):
    first_date = datetime(year, month, day, start_hour, start_minute)
    #datetime string list array
    dtsll = []
    for i in range(num_days):
        start_date = (first_date) + (timedelta(days=i) if weekly == False else timedelta(days=(7*i)))
        end_date = start_date + timedelta(hours=(end_hour - start_hour)) + timedelta(minutes=(end_minute - start_minute))
        if (weekends == False and (start_date.weekday() > 4)):
            continue;

        dtsll.append([dt.strftime('%Y-%m-%d %H:%M:%S') for dt in 
               datetime_range(start_date, end_date, 
               timedelta(minutes=30))])
    return dtsll

def populate_events_table(dbcursor, dtsll):
    check_query = "SELECT id FROM events WHERE start=%s"
    query = "INSERT INTO events (start) VALUES (%s)"
    for dtsl in dtsll:
        for dts in dtsl:
            dbcursor.execute(check_query, (dts,))
            if (len(dbcursor.fetchall()) == 0):
                dbcursor.execute(query, (dts,))
    end_query = "UPDATE events SET end = DATE_ADD(start, INTERVAL 30 minute)"
    dbcursor.execute(end_query)

def is_unreserved(dbcursor, dts):
    check_query_null = "SELECT id FROM events WHERE start=%s AND uid is null"
    dbcursor.execute(check_query_null, (dts,))
    rows = dbcursor.fetchall()
    if (len(rows) == 1):
        return True
    return False
 
def is_reserved(dbcursor, dts, uid = None):
    check_query = "SELECT id FROM events WHERE start=%s AND uid=%s"
    check_query_null = "SELECT id FROM events WHERE start=%s AND uid is not null"
    dbcursor.execute(check_query_null, (dts,)) if uid == None else dbcursor.execute(check_query, (dts,uid,))
    rows = dbcursor.fetchall()
    if (len(rows) == 1):
        return True
    return False

def event_unreserve(dbcursor, dts):
    query = "UPDATE events SET uid = null WHERE start = %s"
    dbcursor.execute(query, (dts,))

def event_reserve(dbcursor, dts, uid):
    query = "UPDATE events SET uid = %s WHERE start = %s"
    dbcursor.execute(query, (uid, dts,))

def event_unreserve_range(dbcursor, dtsll):
    for dtsl in dtsll:
        for dts in dtsl:
            if (is_reserved(dbcursor, dts)):
                event_unreserve(dbcursor, dts)

def event_reserve_range(dbcursor, uid, dtsll):
    for dtsl in dtsll:
        for dts in dtsl:
            if (is_unreserved(dbcursor, dts)):
                event_reserve(dbcursor, dts, uid)

def set_winter_schedule(dbcursor):
     # these are the settings for Winter 2018
    year = 2018
    month = 1
    day = 8
    start_hour = 8
    start_minute = 0
    end_hour = 20
    end_minute= 00
    num_days = 70
    weekends=False
    
    dtsll = datetime_range_strings(year, month, day, start_hour, start_minute, end_hour, end_minute, num_days, weekends)
    #populate events table and set all to reserved by me
    populate_events_table(dbcursor, dtsll)
    event_reserve_range(dbcursor, 1, dtsll)

    m_ava = datetime_range_strings(year, month, day, 18, 0, 20, 0, num_days, weekends, True)
    t_ava = datetime_range_strings(year, month, day+1, 18, 0, 20, 0, num_days, weekends, True)
    w_ava = datetime_range_strings(year, month, day+2, 14, 0, 15, 30, num_days, weekends, True)
    th_ava = datetime_range_strings(year, month, day+3, 18, 0, 20, 0, num_days, weekends, True)
    f_ava = datetime_range_strings(year, month, day+4, 17, 0, 20, 0, num_days, weekends, True)
    event_unreserve_range(dbcursor, m_ava)
    event_unreserve_range(dbcursor, t_ava) 
    event_unreserve_range(dbcursor, w_ava)
    event_unreserve_range(dbcursor, th_ava)
    event_unreserve_range(dbcursor, f_ava)
    
def populate_spring(dbcursor):
    # these are the settings for Spring 2018
    year = 2018
    month = 4
    day = 2
    start_hour = 8
    start_minute = 0
    end_hour = 20
    end_minute = 0
    num_days = (10*7)
    weekends = False

    dtsll = datetime_range_strings(year, month, day, start_hour, start_minute, end_hour, end_minute, num_days, weekends)
    #populate events table and set all to reserved by me
    populate_events_table(dbcursor, dtsll)
    event_reserve_range(dbcursor, 1, dtsll)

def week_begin(dt):
    td = (dt.weekday() + 1) % 7
    return (dt - timedelta(days=td))

def week_begin_string(dt):
    return week_begin(dt).strftime('%Y-%m-%d 00:00:00')
    
def week_end(dt):
    td = 6 - ((dt.weekday() + 1) % 7)
    return (dt + timedelta(days=td))

def week_end_string(dt):
    return week_end(dt).strftime('%Y-%m-%d 23:59:59')

def day_begin_string(dt):
    return dt.strftime('%Y-%m-%d 00:00:00')

def day_end_string(dt):
    return dt.strftime('%Y-%m-%d 23:59:59')

def get_day_events(dbcursor, dt):
    query = "SELECT * FROM events WHERE start BETWEEN %s AND %s"
    start_s = day_begin_string(dt)
    end_s = day_end_string(dt)
    dbcursor.execute(query, (start_s, end_s,))
    return dbcursor.fetchall()

def get_week_events(dbcursor, dt):
    st = week_begin(dt)
    days = []
    for i in range(7):
        days.append(get_day_events(dbcursor, st+timedelta(days=i)))
    return days

def get_user_future_events(dbcursor, uid):
    query = "SELECT * FROM events WHERE uid = %s AND start > %s"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dbcursor.execute(query, (uid, now,))
    return dbcursor.fetchall()


