import os

def format(active, text, type, times, used_times = []):
    # type = 'date' Проверка дня
    # type  = 'time' Проверка времени
    if type == 'time_start':
        if text not in times:
            print(1/0)
        else:
            if used_times[times.index(text)] == '1' and used_times[times.index(text)+1] == '1':
                print(1/0)
    elif type == 'time_end':
        # print(used_times)
        if text not in times:
            print(1/0)
        else:
            if used_times[times.index(text)] == '1' and used_times[times.index(text)-1] == '1':
                print(1/0)
            elif times.index(text) - times.index(active[1][1][0]) >6:
                print(1/0)
            else:
                for i in range(times.index(text) - times.index(active[1][1][0]) - 1):
                    # print(used_times[times.index(text) + i + 1])
                    if used_times[times.index(active[1][1][0]) + i + 1] == '1':
                        print(1/0)

    if type == 'date':
        if not 1 <= int(text.strip().split()[0]) <= 31:
            print(1/0)

def count_for_userid(user_id, scan_days):
    a = 0
    all_days = list(scan_days)
    for i in range(len(all_days)):
        count_this_day = scan_days[all_days[i]][1][0].count(user_id)
        a+=count_this_day
    return a