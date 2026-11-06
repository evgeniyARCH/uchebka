import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime, timedelta
import copy
from models import actual_datetime as ad
from models import scan_days_wash as sd
import os
from models import format_wash

# API-ключ созданный ранее
# token = "vk1.a._nf9C7t0KwBh6HzJM3gQkN4lgNf_qPya2oUqvbULK9E4qHYWXXrTF7kcX6AdFUXiCTdfbK3chprQLYXRgHcdLaH0Uc2uKMA8kv1pNirw3vg_Az0MLDHFX5eVD_J-eXYIMh5Ec2hxn3bGePkHomo24aug-i8xjTJIFTWImFYqD1V61ynHiv54c9qwGmkp_pUfwQTpBzbS1rfnugigjrzzRw"
# token = "vk1.a.boY8K7k2aFtc3I4KLKfFNvTIFV3bXlVxN9gmC-cfwfb7x7Q1iU6I_AwzijgDdTztPYuO_UwmQkD0l6_OszDVNp8oMjPkP3Ijagb-6pN_3w0ZrNEVE6oTKBlMXNQeyIP_KktLmjygAQTg5-TgudQk9HMXNGoa0H2ddg22xoa_yZ-R198rij4MaXcvsPIbh6Sxvu79MADs6NyJNPWKP1tpyA"
# Авторизуемся как сообщество
# vk = vk_api.VkApi(token=token)


class Vk_otvets_st():
    # def __init__(self, request, user_id, active):
    #     super().__init__(request, user_id, active)

    def o_menu_admin(self):
        return 'Добро пожаловать в Админский режим. \nДля дальнейших действий выбери функцию из предложенного списка'

    def o_admin_day(self):

        keys = list(self.scan_days_full)
        res = ''
        a = 1
        for i in range(len(self.scan_days_full)):
            res += str(i) + ' ' + str(keys[i]) + '\n'
            cur_d = self.scan_days_full[keys[i]]
            
            for x in range(len(cur_d[1][0])):
                # user = []
                # user = vk.method("users.get", {"user_ids": cur_d[1][0][x]})
                # user_name = user[0]['last_name']
                res+= str(x) + ' ' + str(cur_d[1][1][x]) + ' - ' + str(cur_d[1][2][x]) + ' @id' + str(cur_d[1][0][x]) + '\n'
                a+=1

            res+='\n'
        if res == '': return 'Записей нет'
        return res

    def o_admin_del(self):
        return 'Теперь введи номер нужного дня и строки в формате "1 2" (БЕЗ КАВЫЧЕК)'

    def o_admin_logs(self):
        f = open('./logs.txt', 'r', encoding='utf-8')
        res ='Логи\n' + f.read()
        f.close()
        return res

    def o_zapis(self): # Запись на стирку
        res = '"Запись на стирку"\n\n'
        # if self.count_user <1:
        res += 'Выберите день стирки или просмотрите свои текущие записи'
        # else:
        #     res += 'К сожалению, у вас есть запись на ближайшие 7 дней. \nДля возможности создать новую запись удалите одну из своих записей'
        tabl = '\n\nКоличество свободных мест по дням\n\n'
        keys = list(self.scan_days)
        # if self.count_user < 1:
        for i in range(5):
            tabl += '---' + keys[i] + ' ' + ad.week(keys[i], 2026) + '---\n'
            tabl += 'Свободных ячеек: ' + str(18 - len(self.scan_days[keys[i]][1][0])) + '\n\n'

        res += tabl
        return res

    def o_zapis_day(self):
        return "Выберите день для записи на стирку."


    def o_start_time(self, c_c): # После выбора дня
        res = 'Выберите время начала стирки.'
        if c_c == 0:
            res = 'К сожалению, уже всё разобрали. Нажмите "Назад" и выберите другой день'
        elif c_c == 2:
            dt = format_wash.detect_zap(self.user_id, self.active, self.scan_days_full)
            res = f'Запись на этот день недоступна, т.к. Вы достигли недельного лимита \n\nВы уже записались на {dt[1]} с {dt[2][0]} до {dt[2][1]}\n\nВ следующий раз Вы сможете записаться на стирку, когда станет доступным {sd.add_date(dt[1], 7, 2026)} \n\nУдалите запись, чтобы перезаписаться или подождите разрешенной даты'
        
        if self.scan_days[self.active[self.user_id][1][0]][1][0] != []:
            
            times = []
            data, time = ad.act_day()
            if data != self.active[self.user_id][1][0]:
                time = '00:01'
            for i in range(len(self.scan_days[self.active[self.user_id][1][0]][1][0])):
                #if self.scan_days[self.active[self.user_id][1][0]][1][1][i] >= time: # or (i < len(self.scan_days[self.active[self.user_id][1][0]][1][0])-1 and self.scan_days[self.active[self.user_id][1][0]][1][1][i+1] >= time and self.scan_days[self.active[self.user_id][1][0]][1][1][i] < time) or (i == len(self.scan_days[self.active[self.user_id][1][0]][1][0])-1 and self.scan_days[self.active[self.user_id][1][0]][1][1][i] < time):
                times.append(datetime.strptime(self.scan_days[self.active[self.user_id][1][0]][1][1][i], "%H:%M")) 
                
            if times != []: res+= '\n\nНиже указано время, которое уже занято на этот день:\n'

            for x in range(len(times)):
                
                res+= '\n' + str(x+1) + '. ' + self.scan_days[self.active[self.user_id][1][0]][1][1][times.index(min(times))] + ' - ' + self.scan_days[self.active[self.user_id][1][0]][1][2][times.index(min(times))]
                if self.scan_days[self.active[self.user_id][1][0]][1][0][times.index(min(times))] == self.user_id:
                    res+= ' - Ваша запись'
                else:
                    # user = []
                    # user = vk.method("users.get", {"user_ids": (self.scan_days[self.active[self.user_id][1][0]][1][0][times.index(min(times))])})
                    # user_name = user[0]['last_name']
                    res+= ' - @id' + str(self.scan_days[self.active[self.user_id][1][0]][1][0][times.index(min(times))])
                times[times.index(min(times))] = datetime.strptime('23:59', "%H:%M")

        return res
    
    # def o_end_time(self): # После выбора дня
    #     return 'Выберите время окончания брони. \n\nВы можете воспользоваться кнопками или ввести точное время с клавиатуры (в формате 10:53) \n\nЕсли пропали кнопки - нажмите на квадрат с четырмя точками левее эмодзи'
    
    def o_post_time(self):
        res = f'Вы хотите записаться на стирку на {self.active[self.user_id][1][0]} с {self.active[self.user_id][1][1][0]}? \nЕсли да, нажмите "Подтвердить". \nЕсли нет, нажмите "Назад"\n\nВ следующий раз Вы сможете записаться на стирку, когда станет доступным {sd.add_date(self.active[self.user_id][1][0], 7, 2026)}'
        return res
    
    def o_write(self):
        res = f'Вы успешно записались на стирку {self.active[self.user_id][1][0]} с {self.active[self.user_id][1][1][0]}. \nДля новой записи нажмите "Начать"\nДля просмотра ваших записей нажмите "Посмотреть мои текущие записи"'
        return res
    
    def o_check_my(self):
        keys = list(self.scan_days)
        res = ''
        a = 1
        for i in range(len(self.scan_days)):
            cur_d = self.scan_days[keys[i]]
            
            for x in range(len(cur_d[1][0])):
                if cur_d[1][0][x] == self.user_id:
                    res+= str(a) + '. ' + str(keys[i]) + '; ' + str(cur_d[1][1][x]) + ' - ' + str(cur_d[1][2][x]) + '\n'
                    a+=1
        if res == '': return 'Записей нет'
        return res

    def o_del(self):
        return 'Выберите запись, которую хотите удалить' 
    
    def o_s_del(self):
        return 'Запись успешно удалена. \nДля новой записи нажмите "Начать"' 









class Vk_keys_st():
    # def __init__(self, request, user_id, active):
    #     super().__init__(request, user_id, active)

    # COLORS:
    # PRIMARY - синий
    # SECONDARY - белый/черный
    # POSITIVE - зеленый
    # NEGATIVE - красный

    # Команды для клавиатуры:
    # vk_keyboard = VkKeyboard() - Создание клавиатуры (ОБЯЗАТЕЛЬНО)
    # keyboard = vk_keyboard.get_empty_keyboard() - Возврат пустой клавиатуры
    # vk_keyboard.add_line() - Переход следующей кнопки на строчку ниже
    # vk_keyboard.add_button('Выход', payload={'type': 'text'}, color=VkKeyboardColor.NEGATIVE) - Добавление кнопки
    # keyboard = vk_keyboard.get_keyboard()  - Активация (возврат) клавиатуры (ОБЯЗАТЕЛЬНО (кроме случая вызова пустой клавиатуры))
    
    def k_empty(self):
        vk_keyboard = VkKeyboard()
        keyboard = vk_keyboard.get_empty_keyboard()
        return keyboard

    def k_menu_admin(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Посмотреть все записи', payload={'type': 'text'}, color=VkKeyboardColor.NEGATIVE)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_admin_day(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Удалить строку', payload={'type': 'text'}, color=VkKeyboardColor.NEGATIVE)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_prev(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_nachat(self):
        vk_keyboard = VkKeyboard()
        # vk_keyboard.add_line()
        vk_keyboard.add_button('Начать', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_zapis(self):
        vk_keyboard = VkKeyboard()
        # if self.count_user <1:
        vk_keyboard.add_button('Выбрать день', payload={'type': 'text'}, color=VkKeyboardColor.POSITIVE)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Посмотреть мои текущие записи', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        if self.user_id in self.ADMINS: 
            vk_keyboard.add_line()
            vk_keyboard.add_button('Админский режим', payload={'type': 'text'}, color=VkKeyboardColor.NEGATIVE)
            vk_keyboard.add_line()
            vk_keyboard.add_button('Посмотреть логи', payload={'type': 'text'}, color=VkKeyboardColor.NEGATIVE)
        # vk_keyboard.add_line()
        # vk_keyboard.add_button('Посмотреть все свободные записи', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_day(self):
        vk_keyboard = VkKeyboard()
        all_items_0 = os.listdir('./stirka/days')
        all_items = sd.sort(all_items_0)
        for i in range(len(all_items)):
            day = all_items[i].strip().split('.')[0]
            if i >= 6:
                vk_keyboard.add_button('' + day, payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
                vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard
    
    def k_start_time(self):
        vk_keyboard = VkKeyboard()
        c = 1

        # if self.scan_days[self.active[self.user_id][1][0]][1][0].count(self.user_id) >= 1 and self.user_id not in self.ADMINS:
        if not format_wash.detect_zap(self.user_id, self.active, self.scan_days_full)[0] or not self.count_user < 1:
            self.active[self.user_id][1][2] = False
            c = 2
        else:
            self.active[self.user_id][1][2] = True

            b = 0
            b_b = 0
            d = True
            day = self.active[self.user_id][1][0]
            r = 0
            data, time = ad.act_day()
            if data != self.active[self.user_id][1][0]:
                time = '00:01'
            while d:

                
                if  (datetime.strptime('06:00', "%H:%M") + timedelta(hours=1*b)) < datetime.strptime(time, "%H:%M"):
                    r = 1
                else:
                    for x in range(len(self.scan_days[day][1][0])):
                        if datetime.strptime(self.scan_days[day][1][1][x], "%H:%M") == (datetime.strptime('06:00', "%H:%M") + timedelta(hours=1*b)):
                            r = 1
                
                
                if r == 0:
                    vk_keyboard.add_button(datetime.strftime(datetime.strptime('06:00', "%H:%M") + timedelta(hours=1*b), "%H:%M"), payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
                    b_b+=1
                    if b_b == 5:
                        vk_keyboard.add_line()
                        b_b = 0
                r = 0
                if datetime.strftime(datetime.strptime('06:00', "%H:%M") + timedelta(hours=1*b), "%H:%M") == '23:00': d = False
                b+=1

            if b_b != 0: vk_keyboard.add_line()

            day = self.active[self.user_id][1][0]
            a = 0
            if self.scan_days[day][1][0] != [] and min(self.scan_days[day][1][1]) == '06:00' and max(self.scan_days[day][1][1]) == '23:00':
                t_list = copy.deepcopy(self.scan_days[day][1])
                del t_list[1][t_list[1].index(min(t_list[1]))]
                for i in range(len(t_list[1])):
                    if t_list[1][i] in t_list[2]: a+=1
                if a == len(t_list[1]):
                    c = 0

        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()

        return keyboard, c
    
   

    def k_post_time(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Подтвердить', payload={'type': 'text'}, color=VkKeyboardColor.POSITIVE)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_write(self):
        
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Начать', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Посмотреть мои текущие записи', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard
    
    def k_check_my(self, otvet):
        vk_keyboard = VkKeyboard()
        if otvet != 'Записей нет':
            vk_keyboard.add_button('Удалить запись', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
            vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard
    
    def k_del(self):
        vk_keyboard = VkKeyboard()

        keys = list(self.scan_days)
        res = ''
        a = 1
        b = 0
        for i in range(len(self.scan_days)):
            cur_d = self.scan_days[keys[i]]
            
            for x in range(len(cur_d[1][0])):
                if cur_d[1][0][x] == self.user_id:
                    res = str(a) + '. ' + str(keys[i]) + '; ' + str(cur_d[1][1][x]) + ' - ' + str(cur_d[1][2][x]) 
                    # res = str(a)
                    if b == 1:
                        vk_keyboard.add_line() 
                        b = 0
                    b+=1
                    vk_keyboard.add_button('' + res, payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
                    a+=1
        vk_keyboard.add_line() 
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard