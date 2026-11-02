import datetime
from time import sleep
import os

mouth_slov = {
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

def act_day():
    global mouth_slov
    now = datetime.datetime.now()
    day = now.strftime('%d')
    mouth = now.strftime('%m')
    mouth_str = mouth_slov[mouth]
    data = day + ' ' + mouth_str
    time = now.strftime('%H:%M')
    return data, time

def create(path, start, numbers):
    for i in range(numbers):
        global mouth_slov
        next_day = datetime.datetime.strptime(start, '%d.%m.%Y') + datetime.timedelta(days=i)
        day = next_day.strftime('%d')
        mouth = next_day.strftime('%m')
        mouth_str = mouth_slov[mouth]
        data = day + ' ' + mouth_str
        f = open(path + data + '.txt', 'w', encoding='utf-8')
        f.close()

def add_new_days():
    global mouth_slov
    while True:
        data, time = act_day()
        if time == '00:01':
            
            try:
                old_day = datetime.datetime.now() - datetime.timedelta(days=1)
                day = old_day.strftime('%d')
                mouth = old_day.strftime('%m')
                mouth_str = mouth_slov[mouth]
                data = day + ' ' + mouth_str
                os.remove('./days/' + data + '.txt')

                next_day = datetime.datetime.now() + datetime.timedelta(days=4)
                day = next_day.strftime('%d')
                mouth = next_day.strftime('%m')
                mouth_str = mouth_slov[mouth]
                data = day + ' ' + mouth_str
                f = open('./days/' + data + '.txt', 'w', encoding='utf-8')
                f.close()


                old_day = datetime.datetime.now() - datetime.timedelta(days=7)
                day = old_day.strftime('%d')
                mouth = old_day.strftime('%m')
                mouth_str = mouth_slov[mouth]
                data = day + ' ' + mouth_str
                os.remove('./stirka/days/' + data + '.txt')

                next_day = datetime.datetime.now() + datetime.timedelta(days=4)
                day = next_day.strftime('%d')
                mouth = next_day.strftime('%m')
                mouth_str = mouth_slov[mouth]
                data = day + ' ' + mouth_str
                f = open('./stirka/days/' + data + '.txt', 'w', encoding='utf-8')
                f.close()

                # f = open('./logs.txt', 'w', encoding='utf-8')
                # f.close()
                print('Пора')
            except:
                pass
            
        # else: print('Еще рано')
        sleep(5)

def week(day, year):
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

    week = {
        '1': "(пн)",
        '2': "(вт)",
        '3': "(ср)",
        '4': "(чт)",
        '5': "(пт)",
        '6': "(сб)",
        '7': "(вс)",
    }
    n_day = day.strip().split(' ')[0]
    mouth = mouth_slov[day.strip().split(' ')[1]]
    y = datetime.datetime.strptime((n_day + '.' + mouth + '.' + str(year)), '%d.%m.%Y')
    return week[str(y.weekday()+1)]
    

# add_new_days()
# create(path = './days/', start= '31.10.2026', numbers= 5)