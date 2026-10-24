import os
from datetime import datetime, timedelta

def format_time(user_id, active, request, scan_days, type, admins):
    day = active[user_id][1][0]
    try:
        time_time = datetime.strptime(request, "%H:%M")
    except:
        return False

    if type == 0: # Start_time
        if datetime.strptime('07:00', "%H:%M") <= time_time <= datetime.strptime('22:59', "%H:%M"):
            for i in range(len(scan_days[day][1][0])):
                if (datetime.strptime(scan_days[day][1][1][i], "%H:%M") <= time_time < datetime.strptime(scan_days[day][1][2][i], "%H:%M")):
                    print('Время входит в промежуток')
                    return False
        else:
            return False
        
    if type == 1: # End_time
        if (datetime.strptime('07:01', "%H:%M") <= time_time <= datetime.strptime('23:00', "%H:%M")) and datetime.strptime(active[user_id][1][1][0], "%H:%M") < time_time and ( datetime.strptime(active[user_id][1][1][0], "%H:%M") + timedelta(hours=3) >= time_time or user_id in admins ):
            for i in range(len(scan_days[day][1][0])):
                if (datetime.strptime(scan_days[day][1][1][i], "%H:%M") < time_time <= datetime.strptime(scan_days[day][1][2][i], "%H:%M")):
                    print('Время входит в промежуток')
                    return False
                else:
                    if datetime.strptime(scan_days[day][1][1][i], "%H:%M") > datetime.strptime(active[user_id][1][1][0], "%H:%M") and datetime.strptime(scan_days[day][1][2][i], "%H:%M") < time_time:
                        print('В запись входит другая запись')
                        return False
        else:
            return False


    return True
    # cur_day = active[user_id][1][0]
    # sd_cd = scan_days[cur_day][1]

def count_for_userid(user_id, scan_days):
    a = 0
    all_days = list(scan_days)
    for i in range(len(all_days)):
        count_this_day = scan_days[all_days[i]][1][0].count(user_id)
        a+=count_this_day
    return a