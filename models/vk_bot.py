from models import scan_days_study as days_study
from models import scan_days_wash as days_wash
import copy
from models import format_study
from models import format_wash
from datetime import datetime, timedelta

from models.vk_uchebka_OK import Vk_keys, Vk_otvets
from models.vk_stirka_OK import Vk_keys_st, Vk_otvets_st


class Vk_bot:
    ADMINS = (214262849, 548147571)

    def __init__(self):
        self.request = str()
        self.user_id = int()
        self.active = dict()
        # это бесполезная инициализация просто для красоты, чтобы не был пустой init :)

    def __str__(self):
        return f"Запрос {self.request}, ID пользователя {self.user_id}"

    def process_msg(self, request, user_id):
        # print(request)
        self.request = request
        self.user_id = user_id
        self.active = {}
        # active = { user_id: \[ [command1, command2,...], [ day, [n-start, n-end], True/False(Меньше двух записей в день?) ] \] } #NEW
        if self.user_id in self.active:
            if self.active[self.user_id]["mode"] == 'uchebka':
                self.scan_days = days_study.scan_days()
                self.count_user = format_study.count_for_userid(self.user_id, self.scan_days)
            elif self.active[self.user_id]["mode"] == 'stirka':
                self.scan_days, self.scan_days_full = days_wash.scan_days()
                self.count_user = format_wash.count_for_userid(self.user_id, self.scan_days)

        return self.otvet()

    def otvet(self):
        # Значения пустышки
        active = self.active
        otvet = 'Неизвестная команда. \nДля записи в учебку/на стирку нажмите "Начать"'
        keyboard = Vk_keys.k_nachat(self.ADMINS)

        template = {"commands": [], "data": [None, ['', ''], None], "mode": None}

        if self.user_id in active and self.request == 'Назад':
            self.request = active[self.user_id]["commands"][-1]
            del active[self.user_id]["commands"][-1]

        if self.request == 'Начать':
            if self.user_id in active:
                del active[self.user_id]
            active[self.user_id] = copy.deepcopy(template)
            active[self.user_id]["commands"].append('zero')
            otvet = 'Выберите режим - запись в учебку или на стирку'
            keyboard = Vk_keys.k_start()
        elif self.request == 'zero':
            otvet = 'Вы вышли из режима записи. \nДля записи в учебку/на стирку нажми "Начать"'
            del active[self.user_id]

        if self.user_id in active and (
                active[self.user_id]["mode"] == None or active[self.user_id]["mode"] in ('stirka', 'uchebka')):
            if self.request == 'Запись на стирку':
                active[self.user_id]["mode"] = 'stirka'
                self.scan_days, self.scan_days_full = days_wash.scan_days()
                self.count_user = format_wash.count_for_userid(self.user_id, self.scan_days)
                otvet = Vk_otvets_st.o_zapis(self)
                keyboard = Vk_keys_st.k_zapis(self)
            elif self.request == 'Запись в учебку':
                active[self.user_id]["mode"] = 'uchebka'
                self.scan_days = days_study.scan_days()
                self.count_user = format_study.count_for_userid(self.user_id, self.scan_days)
                otvet = Vk_otvets.o_zapis(self)
                keyboard = Vk_keys.k_zapis(self)
            active[self.user_id]["commands"].append('Начать')

        if self.user_id in active and active[self.user_id]["mode"] == 'stirka':
            sucs_stirk = 1
            if self.request == 'Выбрать день':
                active[self.user_id]["commands"].append('Запись на стирку')
                active[self.user_id]["data"][1] = ['', '']
                otvet = Vk_otvets_st.o_zapis_day(self)
                keyboard = Vk_keys_st.k_day(self)
            elif self.request == 'Подтвердить' and active[self.user_id]["data"][0] in self.scan_days and \
                    active[self.user_id]["data"][1][0] != '' and active[self.user_id]["data"][1][
                1] != '' and self.count_user < 1:
                if days_wash.write_ses(active, self.user_id):
                    days_wash.create_log(self.user_id, active, 'Запись')
                    keyboard = Vk_keys_st.k_write(self)
                    otvet = Vk_otvets_st.o_write(self)
                else:
                    otvet = 'На данное время уже записались. Нажмите "Назад" и выберите другое время'
                    keyboard = Vk_keys_st.k_prev(self)

            elif self.request == 'Посмотреть мои текущие записи':
                otvet = Vk_otvets_st.o_check_my(self)
                keyboard = Vk_keys_st.k_check_my(self, otvet)
                active[self.user_id]["commands"].append('Запись на стирку')

            elif self.request == 'Удалить запись':
                active[self.user_id]["commands"].append('Посмотреть мои текущие записи')
                otvet = Vk_otvets_st.o_del(self)
                keyboard = Vk_keys_st.k_del(self)

            elif self.request == 'Админский режим' and (self.user_id in self.ADMINS):
                active[self.user_id]["commands"].append('Запись на стирку')
                otvet = Vk_otvets_st.o_menu_admin(self)
                keyboard = Vk_keys_st.k_menu_admin(self)

            elif self.request == 'Посмотреть логи' and (self.user_id in self.ADMINS):
                active[self.user_id]["commands"].append('Админский режим')
                otvet = Vk_otvets_st.o_admin_logs(self)
                keyboard = Vk_keys_st.k_prev(self)

            elif self.request == 'Посмотреть все записи' and (self.user_id in self.ADMINS):
                active[self.user_id]["commands"].append('Админский режим')
                otvet = Vk_otvets_st.o_admin_day(self)
                keyboard = Vk_keys_st.k_admin_day(self)

            elif self.request == 'Удалить строку' and (self.user_id in self.ADMINS):
                active[self.user_id]["commands"].append('Посмотреть все записи')
                otvet = Vk_otvets_st.o_admin_del(self)
                keyboard = Vk_keys_st.k_prev(self)
            else:
                sucs_stirk = 0

            if sucs_stirk == 0:
                if active[self.user_id]["commands"][-1] == 'Запись на стирку':
                    if self.request in list(self.scan_days):
                        # if format_wash.detect_zap(self.user_id, active, self.scan_days_full):
                        active[self.user_id]["data"][0] = self.request
                        keyboard, c_c = Vk_keys_st.k_start_time(self)
                        if self.request in ['04 ноября', '05 ноября', '06 ноября']:
                            f = open('./reserv/' + self.request + '.txt', 'r', encoding='utf-8')
                            otvet_list = f.read().strip().split('\n')
                            f.close()
                            res = ''
                            res_q = 0
                            if not self.count_user < 1:
                                res_q = 1
                                dt = format_wash.detect_zap(self.user_id, active, self.scan_days_full)
                                res += f'Запись на этот день недоступна, т.к. Вы достигли недельного лимита \n\nВы уже записались на {dt[1]} с {dt[2][0]} до {dt[2][1]}\n\nВ следующий раз Вы сможете записаться на стирку, когда станет доступным {days_wash.add_date(dt[1], 7, 2026)} \n\nУдалите запись, чтобы перезаписаться или подождите разрешенной даты\n\n'
                            for i in range(len(otvet_list)):
                                if i <= 1 and res_q == 0 and len(self.scan_days[self.request][1][1]) == 18:
                                    res += otvet_list[i] + '\n'
                                elif 1 < i <= 3:
                                    if i == 2 and (res_q == 0 and not len(self.scan_days[self.request][1][1]) == 18):
                                        res += 'Выберите время начала стирки\n\n'
                                    res += otvet_list[i] + '\n'
                                else:

                                    st_time = otvet_list[i].strip().split(' - ')[0]

                                    if st_time in self.scan_days[self.request][1][1]:
                                        index_id = self.scan_days[self.request][1][1].index(st_time)
                                        if self.scan_days[self.request][1][0][index_id] == 853767309:
                                            res += otvet_list[i] + '\n'
                                        else:
                                            res += otvet_list[i] + ' @id' + str(
                                                self.scan_days[self.request][1][0][index_id]) + '\n'
                            otvet = res

                        else:
                            otvet = Vk_otvets_st.o_start_time(self, c_c)
                        active[self.user_id]["commands"].append('Выбрать день')
                    else:
                        otvet = 'Вы ввели несуществующий в базе день. \nПопробуйте еще раз'
                        keyboard = Vk_keys_st.k_day(self)

                elif active[self.user_id]["commands"][-1] == 'Выбрать день' and active[self.user_id]["data"][1][
                    0] == '' and self.count_user < 1 and self.active[self.user_id]["data"][2]:
                    if format_wash.format_time(user_id=self.user_id, active=active, request=self.request.strip(),
                                             scan_days=self.scan_days, type=0, admins=self.ADMINS):
                        active[self.user_id]["data"][1][0] = self.request
                        active[self.user_id]["data"][1][1] = datetime.strftime(
                            datetime.strptime(self.request.strip(), "%H:%M") + timedelta(hours=1), "%H:%M")
                        otvet = Vk_otvets_st.o_post_time(self)
                        keyboard = Vk_keys_st.k_post_time(self)
                        active[self.user_id]["commands"].append('Выбрать день')
                    else:
                        otvet = 'Вы ввели некорректное время или время уже занято. \nПопробуйте еще раз'
                        keyboard = Vk_keys_st.k_start_time(self)

                elif active[self.user_id]["commands"][-1] == 'Посмотреть мои текущие записи':
                    # active[self.user_id][1][1][1] = self.request
                    otvet = Vk_otvets_st.o_s_del(self)
                    keyboard = Vk_keys_st.k_nachat(self)
                    active[self.user_id]["commands"].append('Начать')
                    days_wash.del_ses(self.user_id, self.scan_days, self.request)

                    pre_day = self.request.strip().split('. ')
                    day_time = pre_day[1].strip().split('; ')
                    active[self.user_id]["data"][0] = day_time[0].strip()
                    active[self.user_id]["data"][1][0] = day_time[1].split(' - ')[0]
                    active[self.user_id]["data"][1][1] = day_time[1].split(' - ')[1]
                    days_wash.create_log(self.user_id, active, 'Удаление')

                elif active[self.user_id]["commands"][-1] == 'Посмотреть все записи' and (self.user_id in self.ADMINS):
                    # active[self.user_id][1][1][1] = self.request
                    days_wash.del_admin(self.request)
                    otvet = Vk_otvets_st.o_s_del(self)
                    keyboard = Vk_keys_st.k_nachat(self)
                    active[self.user_id]["commands"].append('Начать')

        if self.user_id in active and active[self.user_id]["mode"] == 'uchebka':
            sucs_uch = 1
            if self.request == 'Выбрать день' and self.count_user < 8:
                active[self.user_id]["commands"].append('Запись в учебку')
                active[self.user_id]["data"][1] = ['', '']
                otvet = Vk_otvets.o_zapis_day(self)
                keyboard = Vk_keys.k_day(self)

            elif self.request == 'Подтвердить' and active[self.user_id]["data"][0] in self.scan_days and \
                    active[self.user_id]["data"][1][0] != '' and active[self.user_id]["data"][1][
                1] != '' and self.count_user < 8:
                keyboard = Vk_keys.k_write(self)
                otvet = Vk_otvets.o_write(self)

            elif self.request == 'Посмотреть мои текущие записи':
                otvet = Vk_otvets.o_check_my(self)
                keyboard = Vk_keys.k_check_my(self, otvet)
                active[self.user_id]["commands"].append('Запись в учебку')

            elif self.request == 'Удалить запись':
                otvet = Vk_otvets.o_del(self)
                keyboard = Vk_keys.k_del(self)
                active[self.user_id]["commands"].append('Посмотреть мои текущие записи')

            elif self.request == 'Админский режим' and (self.user_id in self.ADMINS):
                active[self.user_id]["commands"].append('Запись в учебку')
                otvet = Vk_otvets.o_menu_admin(self)
                keyboard = Vk_keys.k_menu_admin(self)

            elif self.request == 'Посмотреть все записи' and (self.user_id in self.ADMINS):
                active[self.user_id]["commands"].append('Админский режим')
                otvet = Vk_otvets.o_admin_day(self)
                keyboard = Vk_keys.k_admin_day(self)

            elif self.request == 'Удалить строку' and (self.user_id in self.ADMINS):
                active[self.user_id]["commands"].append('Посмотреть все записи')
                otvet = Vk_otvets.o_admin_del(self)
                keyboard = Vk_keys.k_prev(self)

            else:
                sucs_uch = 0

            if sucs_uch == 0:
                if active[self.user_id]["commands"][-1] == 'Запись в учебку' and self.count_user < 8:
                    if self.request in list(self.scan_days):
                        active[self.user_id]["data"][0] = self.request
                        keyboard, c_c = Vk_keys.k_start_time(self)
                        otvet = Vk_otvets.o_start_time(self, c_c)
                        active[self.user_id]["commands"].append('Выбрать день')
                    else:
                        otvet = 'Вы ввели несуществующий в базе день. \nПопробуйте еще раз'
                        keyboard = Vk_keys.k_day(self)

                elif active[self.user_id]["commands"][-1] == 'Выбрать день' and active[self.user_id]["data"][1][
                    0] == '' and self.count_user < 8 and self.active[self.user_id]["data"][2]:
                    if format_study.format_time(user_id=self.user_id, active=active, request=self.request.strip(),
                                          scan_days=self.scan_days, type=0, admins=self.ADMINS):
                        active[self.user_id]["data"][1][0] = self.request
                        otvet = Vk_otvets.o_end_time(self)
                        keyboard = Vk_keys.k_end_time(self)
                        active[self.user_id]["commands"].append('Выбрать день')
                    else:
                        otvet = 'Вы ввели некорректное время или время уже занято. \nПопробуйте еще раз'
                        keyboard = Vk_keys.k_start_time(self)

                elif active[self.user_id]["commands"][-1] == 'Выбрать день' and active[self.user_id]["data"][1][
                    1] == '' and self.count_user < 8 and self.active[self.user_id]["data"][2]:
                    if format_study.format_time(user_id=self.user_id, active=active, request=self.request.strip(),
                                          scan_days=self.scan_days, type=1, admins=self.ADMINS):
                        active[self.user_id]["data"][1][1] = self.request
                        otvet = Vk_otvets.o_post_time(self)
                        keyboard = Vk_keys.k_post_time(self)
                        active[self.user_id]["commands"].append('Выбрать день')
                    else:
                        otvet = 'Вы ввели некорректное время или время уже занято. \nПопробуйте еще раз'
                        keyboard = Vk_keys.k_end_time(self)

                elif active[self.user_id]["commands"][-1] == 'Посмотреть мои текущие записи':
                    # active[self.user_id][1][1][1] = self.request
                    otvet = Vk_otvets.o_s_del(self)
                    keyboard = Vk_keys.k_nachat(self)
                    active[self.user_id]["commands"].append('Начать')
                    days_study.del_ses(self.user_id, self.scan_days, self.request)

                elif active[self.user_id]["commands"][-1] == 'Посмотреть все записи' and (self.user_id in self.ADMINS):
                    # active[self.user_id][1][1][1] = self.request
                    days_study.del_admin(self.request)
                    otvet = Vk_otvets.o_s_del(self)
                    keyboard = Vk_keys.k_nachat(self)
                    active[self.user_id]["commands"].append('Начать')
        print(self.active)

        return otvet, keyboard

    '''
    except:
        otvet = 'Неизвестная команда. \nДля записи в учебку/на стирку нажмите "Начать"'
        keyboard = Vk_keys.k_nachat(self)
        if self.user_id in active:
            del active[self.user_id]

    if otvet == 'Неизвестная команда. \nДля записи в учебку/на стирку нажмите "Начать"':
        if self.user_id in active:
            del active[self.user_id]
    '''