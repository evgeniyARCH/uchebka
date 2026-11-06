from datetime import datetime, timedelta

def format_time(user_id, active, request, scan_days, type, admins):
    day = active[user_id]["data"][0]
    try:
        time_time = datetime.strptime(request, "%H:%M")
    except:
        return False

    if type == 0: # Start_time
        if datetime.strptime('06:00', "%H:%M") <= time_time <= datetime.strptime('23:00', "%H:%M") and request.split(':')[1] == '00':
            for i in range(len(scan_days[day][1][0])):
                if datetime.strptime(scan_days[day][1][1][i], "%H:%M") == time_time:
                    print('Время входит в промежуток')
                    return False
        else:
            return False



    return True

def count_for_userid(user_id, scan_days):
    a = 0
    all_days = list(scan_days)
    for i in range(len(all_days)):
        count_this_day = scan_days[all_days[i]][1][0].count(user_id)
        a+=count_this_day
    return a

def detect_zap(user_id, active, scan_days_full):
    keys = list(scan_days_full)
    a = active[user_id]["data"][0]

    for i in range(5):
        if user_id in scan_days_full[ keys[i+6] ][1][0]:
            dd = scan_days_full[ keys[i+6] ]
            return [False, keys[i+6], [dd[1][1][dd[1][0].index(user_id)], dd[1][2][dd[1][0].index(user_id)] ]]
    for i in range(7):
        if user_id in scan_days_full[ keys[ keys.index(a) - 6 + i ] ][1][0]:
            dd = scan_days_full[ keys[ keys.index(a) - 6 + i ] ]
            return [False, keys[ keys.index(a) - 6 + i ], [dd[1][1][dd[1][0].index(user_id)], dd[1][2][dd[1][0].index(user_id)]]]

    
    return [True, '']

