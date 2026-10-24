import os
import copy


def scan_days():
    day = [None, [[], [], []]]
    days = {}
    all_items = os.listdir('./days')
    for i in range(len(all_items)):
        f = open('./days/' + all_items[i], 'r', encoding= 'utf-8') 
        f_list = f.read().strip().split('\n')
        f.close()
        a = all_items[i].strip().split('.')[0]
        days[a] = copy.deepcopy(day)
        # print(f_list)
        # print(day)
        if f_list == ['']:
            pass
        else:
            for x in range(len(f_list)):
                cur_ses = f_list[x]
                cur_ses_list = cur_ses.strip().split('/')
                cur_ses_times = cur_ses_list[0].strip().split(',')
                cur_ses_start = (cur_ses_times[0])
                cur_ses_end = (cur_ses_times[1])
                cur_ses_userid = int(cur_ses_list[1])
                days[a][1][0].append(cur_ses_userid)
                days[a][1][1].append(cur_ses_start)
                days[a][1][2].append(cur_ses_end)

    # print(days)
    return days

def write_ses(active, user_id): 
    f = open('./days/' + active[user_id][1][0] + '.txt', 'a+', encoding='utf-8')
    res = '\n' + str(active[user_id][1][1][0]) + ',' + str(active[user_id][1][1][1]) + '/' + str(user_id)
    f.write(res)
    f.close()
# scan_days()

def del_ses(user_id, scan_days, stroka):
    pre_day = stroka.strip().split('. ')
    day_time = pre_day[1].strip().split('; ')
    day = day_time[0].strip()
    time_start = day_time[1].split(' - ')[0]
    time_end = day_time[1].split(' - ')[1]
    # print(time_start)
    # print(time_end)
    c = 0
    number = 0
    for x in range(len(scan_days[day][1][0])):
        if scan_days[day][1][1][x] == time_start and scan_days[day][1][2][x] == time_end:
            c = 1
            number = x
            break
    if c == 0: print(1/0)

    # print(scan_days[day][1][0][number])
    # print(scan_days[day][1][1][number])
    # print(scan_days[day][1][2][number])
    
    del scan_days[day][1][1][number]
    del scan_days[day][1][2][number]
    del scan_days[day][1][0][number]
    f = open('./days/' + day + '.txt', 'w', encoding='utf-8')
    res = ''
    for i in range(len(scan_days[day][1][0])):
        res+= '\n' + scan_days[day][1][1][i] + ',' + scan_days[day][1][2][i] + '/' + str(scan_days[day][1][0][i])
    f.write(res)
    f.close()

def del_admin(data):
    day = int(data.strip().split()[0])
    time = int(data.strip().split()[1])
    all_items = os.listdir('./days')
    for i in range(len(all_items)):
        f = open('./days/' + all_items[i], 'r', encoding= 'utf-8') 
        f_list = f.read().strip().split('\n')
        f.close()
        if day == i:
            del f_list[time]

        res = ''
        for x in range(len(f_list)):
            res+= '\n' + f_list[x]
        f = open('./days/' + all_items[i], 'w', encoding= 'utf-8') 
        f.write(res)
        f.close()
        
            
