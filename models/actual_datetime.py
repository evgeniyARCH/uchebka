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

def add_new_days():
    global mouth_slov
    while True:
        data, time = act_day()
        if time == '00:01':
            print('Пора')
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
            except:
                pass
            
        else: print('Еще рано')
        sleep(5)

# add_new_days()
