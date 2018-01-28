from datetime import datetime, timedelta

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

def datetime_range_strings(year, month, day, start_hour, start_minute, end_hour, end_minute, num, weekends=True, weekly=False):
    first_date = datetime(year, month, day, start_hour, start_minute)
    #datetime string list array
    dtsdl = []
    for i in range(num):
        start_date = (first_date) + (timedelta(days=i) if weekly == False else timedelta(days=(7*i)))
        end_date = start_date + timedelta(hours=(end_hour - start_hour)) + timedelta(minutes=(end_minute - start_minute))
        if (weekends == False and (start_date.weekday() > 4)):
            continue;

        dtsdl.append([dt.strftime('%Y-%m-%d %H:%M:%S') for dt in 
               datetime_range(start_date, end_date, 
               timedelta(minutes=30))])
    return dtsdl

def populate_events_table(dbcursor, dtsdl):
    check_query = "SELECT id FROM events WHERE start=%s"
    query = "INSERT INTO events (start) VALUES (%s)"
    for dtsd in dtsdl:
        for dts in dtsd:
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

def is_unreserved_id(dbcursor, event_id):
    check_query_null = "SELECT id FROM events WHERE id=%s AND uid is null"
    dbcursor.execute(check_query_null, (event_id,))
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

def is_reserved_id(dbcursor, event_id, uid = None):
    check_query = "SELECT id FROM events WHERE id=%s AND uid=%s"
    check_query_null = "SELECT id FROM events WHERE id=%s AND uid is not null"
    dbcursor.execute(check_query_null, (event_id,)) if uid == None else dbcursor.execute(check_query, (event_id,uid,))
    rows = dbcursor.fetchall()
    if (len(rows) == 1):
        return True
    return False

def event_unreserve(dbcursor, dts):
    query = "UPDATE events SET uid = null WHERE start = %s"
    dbcursor.execute(query, (dts,))

def event_unreserve_id(dbcursor, event_id):
    query = "UPDATE events SET uid = null WHERE id = %s"
    dbcursor.execute(query, (event_id,))

def event_reserve(dbcursor, dts, uid):
    query = "UPDATE events SET uid = %s WHERE start = %s"
    dbcursor.execute(query, (uid, dts,))

def event_reserve_id(dbcursor, event_id, uid):
    query = "UPDATE events SET uid = %s WHERE id = %s"
    dbcursor.execute(query, (uid, event_id,))

def event_unreserve_range(dbcursor, dtsdl):
    for dtsd in dtsdl:
        for dts in dtsd:
            if (is_reserved(dbcursor, dts)):
                event_unreserve(dbcursor, dts)

def event_unreserve_range_id(dbcursor, idl):
    for event_id in idl:
        if (is_reserved_id(dbcursor, event_id)):
            event_unreserve_id(dbcursor, event_id)

def event_reserve_range(dbcursor, uid, dtsdl, force=False):
    for dtsd in dtsdl:
        for dts in dtsd:
            if force == False:
                if is_unreserved(dbcursor, dts):
                    event_reserve(dbcursor, dts, uid)
            else:
                event_reserve(dbcursor, dts, uid)

def event_reserve_range_id(dbcursor, uid, idl, force=False):
    for event_id in idl:
        if is_unreserved_id(dbcursor, event_id):
            if force == False:
                event_reserve_id(dbcursor, event_id, uid)
            else:
                event_reserve_id(dbcursor, event_id, uid)

def set_winter_schedule(dbcursor):
     # these are the settings for Winter 2018
    year = 2018
    month = 1
    day = 8
    start_hour = 8
    start_minute = 0
    end_hour = 20
    end_minute= 00
    num_weeks = 7
    weekends=False
    
    dtsdl = datetime_range_strings(year, month, day, start_hour, start_minute, end_hour, end_minute, num_weeks*7, weekends)
    #populate events table and set all to reserved by me
    populate_events_table(dbcursor, dtsdl)
    event_reserve_range(dbcursor, 1, dtsdl)

    m_ava = datetime_range_strings(year, month, day, 18, 0, 20, 0, num_weeks, weekends, True)
    t_ava = datetime_range_strings(year, month, day+1, 18, 0, 20, 0, num_weeks, weekends, True)
    w_ava = datetime_range_strings(year, month, day+2, 14, 0, 15, 30, num_weeks, weekends, True)
    th_ava = datetime_range_strings(year, month, day+3, 18, 0, 20, 0, num_weeks, weekends, True)
    f_ava = datetime_range_strings(year, month, day+4, 17, 0, 20, 0, num_weeks, weekends, True)
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
    num_weeks = 10
    weekends = False

    dtsdl = datetime_range_strings(year, month, day, start_hour, start_minute, end_hour, end_minute, num_weeks*7, weekends)
    #populate events table and set all to reserved by me
    populate_events_table(dbcursor, dtsdl)
    event_reserve_range(dbcursor, 1, dtsdl)

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

def get_event_fromid(dbcursor, event_id):
    query = "SELECT * FROM events WHERE id = %s"
    dbcursor.execute(query, (event_id,))
    rows = dbcursor.fetchall()
    if len(rows) == 1:
        return rows[0]
    else:
        return None

def get_event_fromstring(dbcursor, dts):
    query = "SELECT * FROM events WHERE start = %s"
    dbcursor.execute(query, (dts,))
    rows = dbcursor.fetchall()
    if len(rows) == 1:
        return rows[0]
    else:
        return None

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

def get_weekly_events(dbcursor, dtsdl):
    events_dl = []
    for dtsd in dtsdl:
        events_d = []
        for dts in dtsd:
            event = get_event_fromstring(dbcursor, dts)
            if event != None:
                events_d.append(event)
        events_dl.append(events_d)
    return events_dl
        
