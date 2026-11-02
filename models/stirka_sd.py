import os
import copy
import datetime
from models import actual_datetime as ad

def sort(all_items):
    mouth_slov = {
    'января': "01",
    'февраля': "02",
    'марта': "03",
    'апреля': "04",
    'мая': "05",
    'июня': "06",
    'июля': "07",
    'августа': "08",
    'сентября': "09",
    'октября': "10",
    'ноября': "11",
    'декабря': "12"
    }

    all_items_new = []
    for i in range(len(all_items)):
        pre_a = all_items[i].strip().split(' ')[1]
        a = pre_a.strip().split('.')[0]
        b = all_items[i].strip().split(' ')[0]
        if len(b) == 1: b= '0'+b
        all_items_new.append(str(mouth_slov[a]) + '.' + str(b))
        # print(all_items[i])

    all_items_result = []
    for x in range(len(all_items)):
        all_items_result.append(all_items[all_items_new.index(min(all_items_new))])
        # print(all_items_new[all_items_new.index(min(all_items_new))])
        all_items_new[all_items_new.index(min(all_items_new))] = '99.99'
    # print(all_items_result)
    return all_items_result


def scan_days():
    day = [None, [[], [], []]]
    days = {}
    days_full = {}
    all_items_0 = os.listdir('./stirka/days')
    all_items = sort(all_items_0)
    for i in range(len(all_items)):
        f = open('./stirka/days/' + all_items[i], 'r', encoding= 'utf-8') 
        f_list = f.read().strip().split('\n')
        f.close()
        a = all_items[i].strip().split('.')[0]
        if i >= 6:
            days[a] = copy.deepcopy(day)
        days_full[a] = copy.deepcopy(day)
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
                if i >= 6:
                    days[a][1][0].append(cur_ses_userid)
                    days[a][1][1].append(cur_ses_start)
                    days[a][1][2].append(cur_ses_end)
                days_full[a][1][0].append(cur_ses_userid)
                days_full[a][1][1].append(cur_ses_start)
                days_full[a][1][2].append(cur_ses_end)

    # print(days)
    # print()
    # print(days_full)
    return days, days_full

def write_ses(active, user_id): 
    f = open('./stirka/days/' + active[user_id][1][0] + '.txt', 'a+', encoding='utf-8')
    f.seek(0)
    a = f.read().strip().split('\n')
    # print(a)
    if a != ['']:
        for i in range(len(a)):
            b = a[i].strip().split(',')[0]
            print(b)
            print(datetime.datetime.strptime(b, '%H:%M') == datetime.datetime.strptime(active[user_id][1][1][0], '%H:%M'))
            if datetime.datetime.strptime(b, '%H:%M') == datetime.datetime.strptime(active[user_id][1][1][0], '%H:%M'):
                f.close()
                return False
    f.seek(0, 2)
    res = '\n' + str(active[user_id][1][1][0]) + ',' + str(active[user_id][1][1][1]) + '/' + str(user_id)
    f.write(res)
    f.close()
    return True
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
    f = open('./stirka/days/' + day + '.txt', 'w', encoding='utf-8')
    res = ''
    for i in range(len(scan_days[day][1][0])):
        res+= '\n' + scan_days[day][1][1][i] + ',' + scan_days[day][1][2][i] + '/' + str(scan_days[day][1][0][i])
    f.write(res)
    f.close()

def del_admin(data):
    day = int(data.strip().split()[0])
    time = int(data.strip().split()[1])
    all_items_0 = os.listdir('./stirka/days')
    all_items = sort(all_items_0)
    for i in range(len(all_items)):
        f = open('./stirka/days/' + all_items[i], 'r', encoding= 'utf-8') 
        f_list = f.read().strip().split('\n')
        f.close()
        if day == i:
            del f_list[time]

        res = ''
        for x in range(len(f_list)):
            res+= '\n' + f_list[x]
        f = open('./stirka/days/' + all_items[i], 'w', encoding= 'utf-8') 
        f.write(res)
        f.close()

def create_log(user_id, active, command):
    f = open('./logs.txt', 'r', encoding='utf-8')
    # f.seek(0)
    a = f.read().strip().split('\n')
    f.close()
    date, time = ad.act_day()
    if a != ['']:
        if len(a) >= 100:
            del a[0]
    a.append(str(date) + '/' + str(time) + ' - ' + str(active[user_id][1][0]) + ': ' + str(active[user_id][1][1][0]) + ' - ' + str(active[user_id][1][1][1]) + ' / @id' + str(user_id) + ' / ' + str(command))
    # res = str(active[user_id][1][0]) + ': ' + str(active[user_id][1][1][0]) + ' - ' + str(active[user_id][1][1][1]) + ' / @id' + str(user_id) + ' / ' + str(command)
    f = open('./logs.txt', 'w', encoding='utf-8')
    res = ''
    for i in range(len(a)):
        res+= '\n' + a[i]
    f.write(res)
    f.close()

def add_date(current_date, delta, year):
    mouth_slov = {
    'января': "01",
    'февраля': "02",
    'марта': "03",
    'апреля': "04",
    'мая': "05",
    'июня': "06",
    'июля': "07",
    'августа': "08",
    'сентября': "09",
    'октября': "10",
    'ноября': "11",
    'декабря': "12"
    }

    mouth_slov_2 = {
    '01': 'января',
    '02': 'февраля',
    '03': 'марта',
    '04': 'апреля',
    '05': 'мая',
    '06': 'июня',
    '07': 'июля',
    '08': 'августа',
    '09': 'сентября',
    '10': 'октября',
    '11': 'ноября',
    '12': 'декабря'
    }
    day = current_date.strip().split(' ')[0]
    mouth = mouth_slov[current_date.strip().split(' ')[1]]
    new_day = datetime.datetime.strptime(f'{day}.{mouth}.{year}', '%d.%m.%Y') + datetime.timedelta(days=delta)
    new_day_str = new_day.strftime('%d') + ' ' + mouth_slov_2[new_day.strftime('%m')]
    return new_day_str