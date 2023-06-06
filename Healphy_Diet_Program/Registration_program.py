from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sqlite3
from email_validator import validate_email, EmailNotValidError
import re


def identification():
    class Email_error(Exception):
        pass

    class Password_error(Exception):
        pass

    class Registration_Window(QMainWindow):
        def __init__(self):
            super().__init__()
            uic.loadUi('Registration_Window.ui', self)
            Registration_Window.setStyleSheet(self, "#MainWindow{border-image:url(regist_img.jpg)}")
            self.save_info.clicked.connect(self.save_data)
            self.flag = False

        def save_data(self):
            try:
                self.reg_mail = self.regist_mail.text()
                self.reg_password = self.regist_password.text()
                self.new_name = self.regist_name.text()
                self.height = self.height_edit.text()
                self.weight = self.weight_edit.text()
                self.age = self.age_edit.text()
                con = sqlite3.connect('Users_information.db')
                cur = con.cursor()

                is_new_account = True
                try:
                    validation = validate_email(self.reg_mail, check_deliverability=is_new_account)
                    self.reg_mail = validation.email
                except EmailNotValidError:
                    raise Email_error
                if len(self.reg_password) <= 15:
                    raise Password_error
                if self.reg_password.isdigit():
                    raise Password_error
                if self.reg_password.isalpha():
                    raise Password_error
                cur.execute(f"""INSERT INTO Users_ids_pswrds(User_mail, User_password, 
                User_name, Weight, Height, Age) VALUES ('{self.reg_mail}', '{self.reg_password}',
                 '{self.new_name}', '{self.weight}', '{self.height}', '{self.age}')""")
                con.commit()
            except Email_error:
                error_message = QMessageBox()
                error_message.setWindowTitle('Неверный E-mail')
                error_message.setText('Ошибка введения E-mailа')
                error_message.setIcon(QMessageBox.Warning)
                error_message.setStandardButtons(QMessageBox.Ok | QMessageBox.Reset)
                error_message.setDefaultButton(QMessageBox.Ok)
                error_message.setInformativeText("Ошибка.Система не нашла ни одного совпадения. Такого E-mailа не "
                                                 "существует или он неправильно введен. Или же он уже зарегистрирован.")
                error_message.setDetailedText("Неверно введен E-mail. Проверьте правильное написание всех символов"
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
                error_message.setInformativeText("Пароль не подходит по критериям, подробнее в детальном описании.")
                error_message.setDetailedText("Проверьте, чтобы Ваш пароль соответствовал всем заданным критериям:"
                                              " 1)Длина пароля больше 15 символов 2) В пароле присутствуют И символы,"
                                              " И буквы. Пароль не может состоять только из цифр или букв")
                error_message.buttonClicked.connect(self.reset_button)
                error_message.exec_()


        def reset_button(self, btn):
            if btn.text() == 'Reset':
                self.regist_mail.setText("")
                self.regist_password.setText("")
                self.regist_name.setText("")
            if btn.text() == 'Ok':
                self.regist_mail.setText("Enter your E-mail:")
                self.regist_password.setText("Enter your password:")
                self.regist_name.setText("Enter your name:")


    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        form = Registration_Window()
        form.show()
        sys.excepthook = except_hook
        sys.exit(app.exec())


identification()