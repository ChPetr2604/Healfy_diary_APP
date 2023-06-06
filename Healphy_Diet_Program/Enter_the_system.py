from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sqlite3
import re
from email_validator import validate_email, EmailNotValidError
import time

enter_flag = False
callories = []
diet_str = ''
k = {}


class Create_Error_Message(Exception):  # Создание класса, отвечающего за вызов
    # ошиок при неверном вводе пароля или почты
    pass


class Enter_Window(QMainWindow):  # Это наше основное рабочее окно, с ним связаны все остальные окна и оно отвечает
    # за их обработку, также оно позволяет сверять данные пользователя с системой
    def __init__(self):
        super().__init__()
        uic.loadUi('User_Enter_system.ui', self)
        Enter_Window.setStyleSheet(self, "#MainWindow{border-image:url(digital_identifacation.jpg)}")
        self.Enter_system_btn.clicked.connect(self.enter_account)
        self.identification_btn.clicked.connect(self.connect)
        self.change_psd_btn.clicked.connect(self.change_fun)
        self.flag = False
        self.change_d.clicked.connect(self.connection_change)

    def enter_account(self):  # Эту функцию мы прикрепляем к кнопке входа, она обрабатывает данные и если их нету в БД,
        # то выдает всплывающее окно с рекомендациями, в благоприятном случае предоставляет
        # доступ к двум обрабатывающим окнам и берет значение id пользователя для дальнейшего
        # использования
        try:
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            mails = cur.execute("""SELECT User_mail FROM Users_ids_pswrds""").fetchall()
            passwords = cur.execute("""SELECT User_password FROM Users_ids_pswrds""").fetchall()
            user_ids = cur.execute("""SELECT id FROM Users_ids_pswrds""").fetchall()
            con.close()
            self.enter_mail = self.mail_edit.text()
            self.enter_password = self.password_edit.text()  # В этих строках я забираю данные БД и из вводных полей
            if self.enter_password.isdigit():
                self.enter_password = int(self.enter_password)
            for i in range(len(mails)):
                if mails[i][0] == self.enter_mail and passwords[i][0] == self.enter_password:  # Проверка на наличие
                    # совпадающих логина и пароля и объявление новой вседоступной переменной с id пользователя
                    global user_id
                    user_id = user_ids[i][0]
                    enter_flag = True
                    self.flag = True
                    if enter_flag and user_id == user_ids[i][0]:  # Открытие расчета каллорий при условии совпадающий
                        # id и нахождений совпадений
                        self.myform = Calc_window()
                        self.myform.show()
            if not self.flag:
                raise Create_Error_Message
        except Create_Error_Message:    # Обработка ошибки с паролем и логином
            error_message = QMessageBox()
            error_message.setWindowTitle('Ошибка входа')
            error_message.setText('Неверно введены логин или пароль')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
            error_message.setDefaultButton(QMessageBox.Ok)
            error_message.setInformativeText("Ошибка. Нет совпадений в базе данных. Попробйте ввести логин и"
                                             " пароль снова.")
            error_message.setDetailedText("Неверно введены логин или пароль. В базе данных нет ни одного соотв"
                                          "етствия. Возможно, стоит пройти регистрацию или изменить пароль. Про"
                                          "верьте, чтобы у вас была правильная раскдадка и CapsLock было выключ"
                                          "ено.")
            error_message.buttonClicked.connect(self.reset_button)
            error_message.exec_()

    def connect(self):    # Открытие регистрационного окна и связывание с кнопкой
        self.new_form = Registration_Window()
        self.new_form.show()

    def change_fun(self):    # Открытие окна смены пароля и связывание с кнопкой
        self.change_form = Change_Window()
        self.change_form.show()

    def reset_button(self, btn):    # Функция для кнопки всплыющего окна
        if btn.text() == 'Reset':    # Обработка кнопок окна
            self.mail_edit.setText("")
            self.password_edit.setText("")
        if btn.text() == 'Ok':
            self.mail_edit.setText("Enter your mail:")
            self.password_edit.setText("Enter your password:")

    def connection_change(self):    # Открытие окна составления рациона
        try:
            global user_id
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            user_callories = cur.execute(f"""SELECT caloric_diet FROM
                         Users_ids_pswrds WHERE id = '{user_id}'""").fetchone()
            if user_callories is not None:    # Условие открытия окна
                self.new_form = Change_Diet()
                self.new_form.show()
            else:   # Обработка ошибки
                error = QMessageBox()
                error.setWindowTitle('Ошибка')
                error.setText('Ваших данных по калорийности нет в базк данных')
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
                error.setDefaultButton(QMessageBox.Ok)
                error.setInformativeText(
                    "Пройдите окно выше и выполните рассчеты:)")
                error.buttonClicked.connect(self.reset_button)
                error.exec_()
        except NameError:    # Обработка другой ошибки
            error_message = QMessageBox()
            error_message.setWindowTitle('Ошибка входа')
            error_message.setText('Неверно введены логин или пароль')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
            error_message.setDefaultButton(QMessageBox.Ok)
            error_message.setInformativeText("Ошибка. Нет совпадений в базе данных. Попробйте ввести логин и"
                                             " пароль снова.")
            error_message.setDetailedText("Неверно введены логин или пароль. В базе данных нет ни одного соотв"
                                          "етствия. Возможно, стоит пройти регистрацию или изменить пароль. Про"
                                          "верьте, чтобы у вас была правильная раскдадка и CapsLock было выключ"
                                          "ено.")
            error_message.buttonClicked.connect(self.reset_button)
            error_message.exec_()


class Email_error(Exception):
    pass


class Password_error(Exception):
    pass


class Registration_Window(QMainWindow):    # Окно, отвечающее за регистрацию пользователя и сохранение данных в БД
    def __init__(self):
        super().__init__()
        uic.loadUi('Registration_Window.ui', self)
        Registration_Window.setStyleSheet(self, "#MainWindow{border-image:url(regist_img.jpg)}")
        self.save_info.clicked.connect(self.save_data)
        self.flag = False

    def save_data(self):    # Функция сохранения данных
        try:
            f = False
            self.reg_mail = self.regist_mail.text().lower()
            self.reg_password = self.regist_password.text()
            self.new_name = self.regist_name.text()
            self.height = self.height_edit.text()
            self.weight = self.weight_edit.text()
            self.age = self.age_edit.text()
            if self.reg_password == '' or self.new_name == '' or self.height == '' or self.height == ''\
                    or self.weight == '' or self.age == '':
                raise Password_error
            is_new_account = True
            try:
                validation = validate_email(self.reg_mail, check_deliverability=is_new_account)    # Здесь была
                # инпортирована отдельная библмотека, для проверки существования и корректности почты
                self.reg_mail = validation.email
            except EmailNotValidError:    # Там был собственный класс ошибки, поэтому я еще и свой запихал:)
                raise Email_error
            if len(self.reg_password) <= 15:    # ПРоверка корректности пароля по критериям
                raise Password_error
            if self.reg_password.isdigit():
                raise Password_error
            if self.reg_password.isalpha():
                raise Password_error
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            mails = cur.execute("""SELECT User_mail FROM Users_ids_pswrds""").fetchall()
            for i in mails:   # Проверка на зарегистрированность почты в БД
                if i[0] == self.reg_mail:
                    f = True
            if not f:
                cur.execute(f"""INSERT INTO Users_ids_pswrds(User_mail, User_password, 
                                User_name, Weight, Height, Age) VALUES ('{self.reg_mail}', '{self.reg_password}',
                                 '{self.new_name}', '{self.weight}', '{self.height}', '{self.age}')""")
                con.commit()
                error_message = QMessageBox()
                error_message.setWindowTitle('Ваши данные сохранены в базе данных.')
                error_message.setText('Все данные подтверждены')
                error_message.setIcon(QMessageBox.Information)
                error_message.setStandardButtons(QMessageBox.Ok)
                error_message.setDefaultButton(QMessageBox.Ok)
                error_message.setInformativeText(
                    "Ваши данные сохранены и могут использоваться программой в дальнейшем.")
                error_message.setDetailedText(
                    "Ваш аккаунт настроен и готов к использованию. Приятного пользования!)")
                error_message.buttonClicked.connect(self.reset_button)
                error_message.exec_()
                # добавление данных в БД и ведомление об этом пользователя
            else:
                raise Email_error
        except Email_error:   # Далее следуют виды ошибок и их обработка
            error_message = QMessageBox()
            error_message.setWindowTitle('Неверный E-mail')
            error_message.setText('Ошибка введения E-mailа')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
            error_message.setDefaultButton(QMessageBox.Ok)
            error_message.setInformativeText(
                "Ошибка.Система не нашла ни одного совпадения. Такого E-mailа не "
                "существует или он неправильно введен. Вероятно, он уже зарегистрирован.")
            error_message.setDetailedText(
                "Неверно введен E-mail. Проверьте правильное написание всех символов"
                " и их последовательность. Про"
                "верьте, чтобы у вас была правильная раскдадка и CapsLock было выключ"
                "ено.")
            error_message.buttonClicked.connect(self.reset_button)
            error_message.exec_()
        except Password_error:
            error_message = QMessageBox()
            error_message.setWindowTitle('Неверный формат пароля')
            error_message.setText('Формат пароля неверен. Он не является надёжным.'
                                  ' Или же какие-то поля остаются пустыми')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
            error_message.setDefaultButton(QMessageBox.Ok)
            error_message.setInformativeText(
                "Пароль не подходит по критериям, подробнее в детальном описании. Либо не все поля заполнены")
            error_message.setDetailedText(
                "Проверьте, чтобы Ваш пароль соответствовал всем заданным критериям и все поля были заполнены:"
                " 1)Длина пароля больше 15 символов 2) В пароле присутствуют И символы,"
                " И буквы. Пароль не может состоять только из цифр или букв")
            error_message.buttonClicked.connect(self.reset_button)
            error_message.exec_()

    def reset_button(self, btn):    # Всё та же функция, обрабатывающая кнопки всплывающих окон
        if btn.text() == 'Reset':
            self.regist_mail.setText("")
            self.regist_password.setText("")
            self.regist_name.setText("")
        if btn.text() == 'Ok':
            self.regist_mail.setText("Enter your E-mail:")
            self.regist_password.setText("Enter your password:")
            self.regist_name.setText("Enter your name:")


class Calc_window(QMainWindow):    # Это уже собственно рабочее окно, считающее калории по формуле:)
    def __init__(self):
        super().__init__()
        uic.loadUi('Calculation_Window.ui', self)
        Calc_window.setStyleSheet(self, "#MainWindow{border-image:url(Wallpaper_calc.jpg)}")
        con = sqlite3.connect('Users_information.db')
        cur = con.cursor()
        mails = cur.execute(f"""SELECT User_name FROM Users_ids_pswrds WHERE id = {user_id}""").fetchall()
        self.Greet_label.setText(f'Здравствуйте, {mails[0][0]}')    # Сразу уведомляю пользователя о том, что знаю его
        self.final_label.hide()
        self.progress.setValue(0)
        self.man_rb.toggled.connect(self.on_selected)
        self.woman_rb.toggled.connect(self.on_selected)
        self.helicopter_rb.toggled.connect(self.on_selected)
        self.combo_fitness.activated[str].connect(self.calculation)
        self.sovet_text.hide()

    def on_selected(self):    # Это обработчик для выбора кнопок (RadioButton Group)
        self.name = self.sender()
        if self.name.isChecked():
            self.name = self.name.text()

    def calculation(self):    # Собственно сами расчеты, в зависимости от выбранных параметров
        result = 0
        con = sqlite3.connect('Users_information.db')
        cur = con.cursor()
        weigth = cur.execute(f"""SELECT Weight FROM Users_ids_pswrds WHERE id = {user_id}""").fetchone()
        height = cur.execute(f"""SELECT Height FROM Users_ids_pswrds WHERE id = {user_id}""").fetchone()
        age = cur.execute(f"""SELECT Age FROM Users_ids_pswrds WHERE id = {user_id}""").fetchone()
        # Изъятие данных из БД, для подставления в формулу. А зачем тогда нужна регистрация и учётка?:)))))
        self.active = self.combo_fitness.currentText()
        if self.name == 'Мужчина':
            result = eval(f'66.5 + (13.75 * {weigth[0]}) + (5.003 * {height[0]}) - (6.755 * {age[0]})')
            result *= float(self.active.split()[0]) * 0.95
            for i in range(101):
                self.progress.setValue(i)
                time.sleep(0.1)
            self.final_label.setText(f'Необходимое количество каллорий в день для Вас: {result} Ккал')
            self.final_label.show()
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            cur.execute(f"""UPDATE Users_ids_pswrds SET caloric_diet = '{result}' WHERE id = '{user_id}'""")
            # В каждом из вариантов я обновляию данные по каллорийности пользователя и сохраняю их
            con.commit()
        elif self.name == 'Женщина':
            result = eval(f'655.1 + (9.563 * {weigth[0]}) + (1.850 * {height[0]}) - (4.676 * {age[0]})')
            result *= float(self.active.split()[0]) * 0.95
            for i in range(101):
                self.progress.setValue(i)
                time.sleep(0.1)
            self.final_label.setText(f'Необходимое количество каллорий в день для Вас: {result} Ккал')
            self.final_label.show()
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            cur.execute(f"""UPDATE Users_ids_pswrds SET caloric_diet = '{result}' WHERE id = '{user_id}'""")
            con.commit()
        elif self.name == 'Боевой вертолёт МИ-26':
            result = 3100 * 24 * 7718
            result *= float(self.active.split()[0])
            for i in range(101):
                self.progress.setValue(i)
                time.sleep(0.1)
            self.final_label.setText(f'Необходимое количество каллорий в день для Вас: {3100 * 24 * 7718} Ккал')
            self.final_label.show()
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            cur.execute(f"""UPDATE Users_ids_pswrds SET caloric_diet = '{result}' WHERE id = '{user_id}'""")
            con.commit()
        self.sovet_text.setText(
            f'Сейчас для простого существования в том виде, в котором вы находитесь, вам нужно тратить {result} калорий'
            f' каждый день с учётом фзической активности. Если вы хотите понизить свой вес, то уменьшите дневную норму'
            f' до {result * 0.75} калорий и уже через месяц вы увидите результат. В данном случае вы будете терять по '
            f'1.5 кг в месяц. Если вы хотите НАБИРАТЬ массу, то увеличьте необходимое количество калорий'
            f' до {result + 250}')
        #   Специальный совет, для особо умных
        self.sovet_text.show()


class NoNameMailError(Exception):
    pass


class Change_Window(QMainWindow):    # Смена пароля, ибо не все занимаются записью и памятью
    def __init__(self):
        super().__init__()
        uic.loadUi('Password_Change_Window.ui', self)
        Change_Window.setStyleSheet(self, "#MainWindow{border-image:url(change_img.jpg)}")
        self.saving.setValue(0)
        self.changes_btn.clicked.connect(self.saving_new_data)

    def saving_new_data(self):    # Функция смены
        try:
            self.id = self.get_mail.text()
            self.password = self.new_psd.text()
            self.height = self.new_height.text()
            self.weight = self.new_weight.text()
            self.age = self.new_age.text()
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            pswd = cur.execute(f"""SELECT User_password FROM Users_ids_pswrds
             WHERE User_mail = '{self.id}'""").fetchone()
            is_new_account = True
            try:
                validation = validate_email(self.id, check_deliverability=is_new_account)
                # Опять же проверка существания введенной почты
                self.id = validation.email
            except EmailNotValidError:
                raise Email_error
            if pswd is None:   # Проверка почты на зарегистрированность в БД
                raise NoNameMailError
            if len(self.password) <= 15:    # Проврека пароля по критериям
                raise Password_error
            if self.password.isdigit():
                raise Password_error
            if self.password.isalpha():
                raise Password_error
            if self.password == pswd[0]:   # Проверка совпадения пароля и обработка ошибки
                error_message = QMessageBox()
                error_message.setWindowTitle('Пароли совпадают')
                error_message.setText('Нельзя, чтобы введённые пароли сопадали')
                error_message.setIcon(QMessageBox.Warning)
                error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
                error_message.setDefaultButton(QMessageBox.Ok)
                error_message.setInformativeText(
                    "Ошибка.В системе уже есть такой пароль связанный с этой почтой.")
                error_message.setDetailedText(
                    "Такой пароль уже забит в базу данных под вашим логином. Они не могут совпадать,"
                    " так что, будьте добры,"
                    " смените пароль на другой.")
                error_message.buttonClicked.connect(self.reset_button)
                error_message.exec_()
            else:
                if self.password != pswd[0]:    # Проверка на пустоту поля и сохранение новых данных
                    con = sqlite3.connect('Users_information.db')
                    cur = con.cursor()
                    cur.execute(f"""UPDATE Users_ids_pswrds SET User_password = '{self.password}' 
                    WHERE User_mail = '{self.id}'""")
                    con.commit()
                if self.age != '':
                    con = sqlite3.connect('Users_information.db')
                    cur = con.cursor()
                    cur.execute(f"""UPDATE Users_ids_pswrds SET Age = '{self.age}' 
                    WHERE User_mail = '{self.id}'""")
                    con.commit()
                if self.weight != '':
                    con = sqlite3.connect('Users_information.db')
                    cur = con.cursor()
                    cur.execute(f"""UPDATE Users_ids_pswrds SET Weight = '{self.weight}' 
                    WHERE User_mail = '{self.id}'""")
                    con.commit()
                if self.height != '':
                    con = sqlite3.connect('Users_information.db')
                    cur = con.cursor()
                    cur.execute(f"""UPDATE Users_ids_pswrds SET Height = '{self.height}' 
                    WHERE User_mail = '{self.id}'""")
                    con.commit()
                for i in range(101):   # Очень полезная имитация прогрузки
                    self.saving.setValue(i)
                    if i == 64 and i == 86:
                        time.sleep(2)
                    else:
                        time.sleep(0.1)
                inf_message = QMessageBox()
                inf_message.setWindowTitle('Данные смененфы')
                inf_message.setText('Ваши данные изменены на новые.')
                inf_message.setIcon(QMessageBox.Information)
                inf_message.setStandardButtons(QMessageBox.Ok)
                inf_message.setDefaultButton(QMessageBox.Ok)
                inf_message.setInformativeText(
                    "Данные изменены и полностью готовы к работе.")
                inf_message.setDetailedText(
                    "Смена данных прошла успешно, удачного пользования")
                inf_message.buttonClicked.connect(self.reset_button)
                inf_message.exec_()
        except Email_error:
            error_message = QMessageBox()   # Каждая из ошибок обрабатывает свои случаи, чтобы пользователю проще
            # было понять, где он накосячил
            error_message.setWindowTitle('Неверный E-mail')
            error_message.setText('Ошибка введения E-mailа')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
            error_message.setDefaultButton(QMessageBox.Ok)
            error_message.setInformativeText(
                "Ошибка.Система не нашла ни одного совпадения. Такого E-mailа не "
                "существует или он неправильно введен. Вероятно, он уже зарегистрирован.")
            error_message.setDetailedText(
                "Неверно введен E-mail. Проверьте правильное написание всех символов"
                " и их последовательность. Про"
                "верьте, чтобы у вас была правильная раскдадка и CapsLock было выключ"
                "ено.")
            error_message.buttonClicked.connect(self.reset_button)
            error_message.exec_()
        except Password_error:
            error_message = QMessageBox()
            error_message.setWindowTitle('Неверный формат пароля')
            error_message.setText('Формат пароля неверен. Он не является надёжным.')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
            error_message.setDefaultButton(QMessageBox.Ok)
            error_message.setInformativeText(
                "Пароль не подходит по критериям, подробнее в детальном описании.")
            error_message.setDetailedText(
                "Проверьте, чтобы Ваш пароль соответствовал всем заданным критериям:"
                " 1)Длина пароля больше 15 символов 2) В пароле присутствуют И символы,"
                " И буквы. Пароль не может состоять только из цифр или букв")
            error_message.buttonClicked.connect(self.reset_button)
            error_message.exec_()
        except NoNameMailError:
            error_message = QMessageBox()
            error_message.setWindowTitle('Неверный формат Почты')
            error_message.setText('Такой почты не зарегистрировано.')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
            error_message.setDefaultButton(QMessageBox.Ok)
            error_message.setInformativeText(
                "В базе данных не найдено ни одного упоминания об этой почте.")
            error_message.setDetailedText(
                "Такой почты не обнаружено. Совет: пройдите регистрацию")
            error_message.buttonClicked.connect(self.reset_button)
            error_message.exec_()

    def reset_button(self, btn):
        if btn.text() == 'Reset':
            self.get_mail.setText("")
            self.new_psd.setText("")
            self.new_weight.setText("")
        if btn.text() == 'Ok':
            self.get_mail.setText("Enter your E-mail:")
            self.new_psd.setText("Enter your password:")
            self.new_weight.setText("Enter your name:")


class Caloric_Error(Exception):
    pass


class Change_Diet(QMainWindow):   # Составление рациона, путем выюора из таблицы
    def __init__(self):
        super().__init__()
        uic.loadUi('Diet.ui', self)
        Change_Diet.setStyleSheet(self, "#MainWindow{border-image:url(diet_img.jpg)}")
        con = sqlite3.connect('Users_information.db')
        cur = con.cursor()
        user_callories = cur.execute(f"""SELECT caloric_diet FROM
                     Users_ids_pswrds WHERE id = '{user_id}'""").fetchone()
        self.combo_dishes.activated[str].connect(self.show_table)
        self.get_dishes.clicked.connect(self.getting_dish)
        self.flag = False
        self.show_table()
        self.tableWidget.setHorizontalHeaderLabels(['Название блюда', 'Содержание каллорий'])
        self.tableWidget.resizeColumnsToContents()
        self.reset_diet.clicked.connect(self.clear_diet)
        self.total_cal.display(user_callories[0])
        self.save_diet.clicked.connect(self.diet_saving)
        self.open_diet.clicked.connect(self.opening_diet)

    def show_table(self):   # Функция, заполняющая таблицу для просмотра даннными блюд из БД
        query = self.combo_dishes.currentText()
        con = sqlite3.connect('Users_information.db')
        cur = con.cursor()
        table_vdgt = cur.execute(f"""SELECT dish, caloric_content FROM {query}""")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(table_vdgt):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def getting_dish(self):    # Функция, перемещающая выбраннные элементы в буфер и отображающая в отдельном поле
        try:
            global k
            global diet_str
            global callories
            global user_id
            counter = 1
            selected = [i.text() for i in self.tableWidget.selectedItems()]
            for i in range(0, len(selected), 2):
                k[selected[i]] = selected[i + 1]
                z = selected[i + 1].split()[0]
                z = '.'.join(z.split(','))
                callories.append(float(z))
                # Все элементы сохраняются в словарь, потому что по ключам не может быть повторений и пересекающиеся
                # вопросы не будут отображаться по два раза, а также будет удобно брать калорийность продуктов как
                # значения соответствующие ключам
            for i, j in k.items():    # Тут идет составление списка продуктов на отображение пользователю
                diet_str += f'{counter}. {i} {j} \n'
                counter += 1
            self.diet_edit.setText(diet_str)
            diet_str = ''
            con = sqlite3.connect('Users_information.db')
            cur = con.cursor()
            user_callories = cur.execute(f"""SELECT caloric_diet FROM
             Users_ids_pswrds WHERE id = '{user_id}'""").fetchone()
            if user_callories is None:    # Если у пользователя не зарегистрированы данные о калориях, выпадает ошибка
                raise Caloric_Error
            ost_cal = user_callories[0] - sum(callories)
            if ost_cal >= 0:
                self.remaind_cal.display(ost_cal)    # В поле показывается количество оставшихся на день калорий
            else:    # Веселая ошибка при перебирании калорийности через норму на день
                error_message = QMessageBox()
                error_message.setWindowTitle('Проблема рациона!')
                error_message.setText('Шо то Вы многовато едите для худеющего... -_-')
                error_message.setIcon(QMessageBox.Warning)
                error_message.setStandardButtons(QMessageBox.Cancel)
                error_message.setDefaultButton(QMessageBox.Cancel)
                error_message.setInformativeText("Не, ну правда, я Вас отлично понимаю, но стоит себя держать в руках,"
                                                 " если Вы хотите достичь своей цели... Попробуйте составить свой "
                                                 "рацион заново, я верю, что у Вас всё обязательно получится) Давайте"
                                                 " стараться вместе:)")
                error_message.buttonClicked.connect(self.reset_btn)
                error_message.exec_()
        except ValueError:   # Обработка ошибки, возникающей при выделении неполной строки
            error_message = QMessageBox()
            error_message.setWindowTitle('Ошибка подсчёта каллорийности')
            error_message.setText('Ошибка! Нет выделенного значения калорий!')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Reset | QMessageBox.Cancel)
            error_message.setDefaultButton(QMessageBox.Reset)
            error_message.setInformativeText("Пожалуйста, выдеяйте не только названия,"
                                             " но и значения калорийности продукта")
            error_message.buttonClicked.connect(self.reset_btn)
            error_message.exec_()
        except Caloric_Error:   # Обработка варианта, если у пользователя нет зарегистрированных калорий
            error_message = QMessageBox()
            error_message.setWindowTitle('Ваших данных нету в базе данных')
            error_message.setText('Ошибка! Зарегистрирйте свои данные!')
            error_message.setIcon(QMessageBox.Warning)
            error_message.setStandardButtons(QMessageBox.Reset | QMessageBox.Cancel)

    def clear_diet(self):   # По названию понятно, что кнопка отвечает за полное удаление рациона из окна
        error_message = QMessageBox()
        error_message.setWindowTitle('Очистка рациона')
        error_message.setText('Вы уверены, что хотите удалить свой рацион?')
        error_message.setIcon(QMessageBox.Warning)
        error_message.setStandardButtons(QMessageBox.Reset | QMessageBox.Cancel)
        error_message.setDefaultButton(QMessageBox.Reset)
        error_message.setInformativeText("Вы прямо точно уверены?")
        error_message.buttonClicked.connect(self.reset_btn)
        error_message.exec_()

    def reset_btn(self, btn):   # Обработка кнопок всплывающего окна
        if btn.text() == 'Reset':
            global diet_str
            global k
            k = {}
            diet_str = ''
            self.diet_edit.setText(diet_str)
        elif btn.text() == 'Cancel':
            pass

    def diet_saving(self):    # Особая фишка - сохранение рациона себе в файл, который можно редактировать
        # и перекидывать куда хочешь
        global callories
        con = sqlite3.connect('Users_information.db')
        cur = con.cursor()
        usern = cur.execute(f"""SELECT User_name FROM
                     Users_ids_pswrds WHERE id = '{user_id}'""").fetchone()
        disk = self.diet_edit.toPlainText()
        with open(f"Рацион для пользователя {usern[0]}.txt", mode='w+', encoding='utf8') as file:
            file.write(f'{usern[0]}, Ваш составленный рацион:\n')
            file.write(disk)
            file.write('\n')
            file.write('--------------------------------------\n')
            file.write('\n')
            file.write(f'Общая энергетическая ценность Вашего рациона: {sum(callories)} Ккал')
        # Тут файл сохраняется, а потом пользователь получает об этом уведомление
        information = QMessageBox()
        information.setWindowTitle('Выполнение сохранения...')
        information.setText('Сохранение прошло успешно!')
        information.setIcon(QMessageBox.Information)
        information.setStandardButtons(QMessageBox.Reset | QMessageBox.Cancel)
        information.setDefaultButton(QMessageBox.Reset)
        information.setInformativeText("ВНИМАНИЕ! Ваш файл сохранён в папку программы!")
        information.buttonClicked.connect(self.reset_btn)
        information.exec_()

    def opening_diet(self):   # Тут мы уже открываем файл в формате .txt. Программа не примет файлы,
        # сохраненные не в формате файлов, которые делала эта программа
        global k
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрерите свой файл:', '',
            'Текстовый файл (*.txt);;Все файлы (*)')[0]
        with open(fname, mode='r', encoding='utf8') as f:
            new = f.readlines()
        with open(fname, mode='r', encoding='utf8') as f:
            importing_file = f.read()
        new = new[1:-5]
        self.diet_edit.setText(importing_file)    # А здесь мы выводим открытый файл пользователю
        for i in range(len(new)):
            k[' '.join(new[i].split()[1:-2])] = ' '.join(new[i].split()[-2:])   # Здесь происходит забивание значение в
            # словарь, в дальнейшем рацион можно сохранять, но для редактирования придётся удалить рацион


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Enter_Window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
