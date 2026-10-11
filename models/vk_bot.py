import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from models import actual_datetime as ad
from models import scan_days as sd
import os
import copy

class Vk_bot:
    def __init__(self, request, user_id, active, scan_days):
        self.request = request
        self.user_id = user_id
        self.active = active
        self.scan_days = scan_days

    # active = { user_id: [[command1, command2,...], [day, stiralka, time, command(delete/create)]], user_name, tabl} #OLD 
    # active = { user_id: [[command1, command2,...], [day, [n-start, n-end], command(delete/create)]]} #NEW
    
    def __str__(self):
        return f"Запрос {self.request}, ID пользователя {self.user_id}"

    def otvet(self):

        # Значения пустышки
        active = self.active
        otvet = 'Неизвестная команда. \nТы всегда можешь записаться в учебку:))'
        keyboard = Vk_keys.k_nachat(self)

        primer_list = [[], [None, ['', ''], None]]

        if self.user_id in active:
            sucs = 1
            if self.request == 'Назад':
                self.request = active[self.user_id][0][-1]
                del active[self.user_id][0][-1]
            if self.request == 'Выбрать день':
                active[self.user_id][0].append('Запись в учебку')
                active[self.user_id][1][1] = ['', '']
                otvet = Vk_otvets.o_zapis(self)
                keyboard = Vk_keys.k_day(self)

            elif self.request == 'Подтвердить':
                keyboard = Vk_keys.k_write(self)
                otvet = Vk_otvets.o_write(self)

            elif self.request == 'Посмотреть все мои записи':
                otvet = Vk_otvets.o_check_my(self)
                keyboard = Vk_keys.k_check_my(self, otvet)
                active[self.user_id][0].append('Запись в учебку')

            elif self.request == 'Удалить запись':
                otvet = Vk_otvets.o_del(self)
                keyboard = Vk_keys.k_del(self)
                active[self.user_id][0].append('Посмотреть все мои записи')

            else:
                sucs = 0

        if self.request == 'Начать' or self.request == 'Запись в учебку':
            # active[self.user_id] = primer_list.copy()
            if self.user_id in active:
                del active[self.user_id]
            active[self.user_id] = copy.deepcopy(primer_list)
            active[self.user_id][0].append('zero')
            otvet = Vk_otvets.o_zapis(self)
            keyboard = Vk_keys.k_zapis(self)

        elif self.request == 'zero':
            otvet = 'Дальше назад пути нет!'

        else:
            if self.user_id in active and sucs == 0:

                if active[self.user_id][0][-1] == 'Запись в учебку':
                    active[self.user_id][1][0] = self.request
                    otvet = Vk_otvets.o_start_time(self)
                    keyboard = Vk_keys.k_start_time(self)
                    active[self.user_id][0].append('Выбрать день')

                elif active[self.user_id][0][-1] == 'Выбрать день' and active[self.user_id][1][1][0] == '':
                    active[self.user_id][1][1][0] = self.request
                    otvet = Vk_otvets.o_end_time(self)
                    keyboard = Vk_keys.k_end_time(self)
                    active[self.user_id][0].append('Выбрать день')

                elif active[self.user_id][0][-1] == 'Выбрать день' and active[self.user_id][1][1][1] == '':
                    active[self.user_id][1][1][1] = self.request
                    otvet = Vk_otvets.o_post_time(self)
                    keyboard = Vk_keys.k_post_time(self)
                    active[self.user_id][0].append('Выбрать день')

                elif active[self.user_id][0][-1] == 'Посмотреть все мои записи':
                    # active[self.user_id][1][1][1] = self.request
                    otvet = Vk_otvets.o_s_del(self)
                    keyboard = Vk_keys.k_prev(self)
                    active[self.user_id][0].append('Начать')
                    sd.del_ses(self.user_id, self.scan_days, self.request)



        


        print(self.active)

        return [otvet,keyboard, active]





class Vk_otvets(Vk_bot):
    def __init__(self, request, user_id, active):
        super().__init__(request, user_id, active)

    def o_zapis(self): # Запись на стирку
        return 'Выбери необходимый вариант из меню'
    
    def o_start_time(self): # После выбора дня
        return 'Теперь выбери начало записи'
    
    def o_end_time(self): # После выбора дня
        return 'Теперь выбери конец записи'
    
    def o_post_time(self):
        return 'Ты уверен?'
    
    def o_write(self):
        return 'Всё зафиксировано'
    
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
        return 'Впиши номер записи, которую хочешь удалить'
    
    def o_s_del(self):
        return 'Удалено успешно'









class Vk_keys(Vk_bot):
    def __init__(self, request, user_id, active):
        super().__init__(request, user_id, active)

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

    def k_prev(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_nachat(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Начать', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_zapis(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Выбрать день', payload={'type': 'text'}, color=VkKeyboardColor.POSITIVE)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Посмотреть все мои записи', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        # vk_keyboard.add_line()
        # vk_keyboard.add_button('Посмотреть все свободные записи', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_day(self):
        vk_keyboard = VkKeyboard()
        all_items = os.listdir('./days')
        for i in range(len(all_items)):
            day = all_items[i].strip().split('.')[0]
            vk_keyboard.add_button(day, payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
            vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard
    
    def k_start_time(self):
        vk_keyboard = VkKeyboard()
        times = self.scan_days[self.active[self.user_id][1][0]][0]
        date_tm = self.scan_days[self.active[self.user_id][1][0]][2]
        b = 0
        data, time = ad.act_day()
        for y in range(len(times)-1):
            if times[y] == '0' and self.scan_days[self.active[self.user_id][1][0]][2][y] >= time:
                if b == 5:
                    b = 1
                    vk_keyboard.add_line()
                else:
                    b+=1
                vk_keyboard.add_button(date_tm[y], payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard
    
    def k_end_time(self):
        vk_keyboard = VkKeyboard()
        times = self.scan_days[self.active[self.user_id][1][0]][0]
        date_tm = self.scan_days[self.active[self.user_id][1][0]][2]
        c = True
        indx = date_tm.index(self.active[self.user_id][1][1][0])
        a = 1
        while c:
            if (indx+a <= len(times)-2 and a<=5) and times[indx+a] == '0':
                a+=1
            else:
                # a+=1
                c = False

        b = 0
        for i in range(a):
            if b == 5:
                b = 1
                vk_keyboard.add_line()
            else:
                b+=1
            vk_keyboard.add_button(date_tm[indx+i+1], payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_post_time(self):
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Подтвердить', payload={'type': 'text'}, color=VkKeyboardColor.POSITIVE)
        vk_keyboard.add_line()
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard

    def k_write(self):
        sd.write_ses(self.active, self.user_id)
        vk_keyboard = VkKeyboard()
        vk_keyboard.add_button('Начать', payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
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
                    vk_keyboard.add_button(res, payload={'type': 'text'}, color=VkKeyboardColor.PRIMARY)
                    a+=1
        vk_keyboard.add_line() 
        vk_keyboard.add_button('Назад', payload={'type': 'text'}, color=VkKeyboardColor.SECONDARY)
        keyboard = vk_keyboard.get_keyboard()
        return keyboard