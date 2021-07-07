import sys
import math
import re
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic


class App(QWidget):
    f_num = ''      # first number
    s_num = ''      # second number
    op_sign = ''    # operation sign
    op_result = ''  # operation result

    def __init__(self):
        self.start()
        self.set()

    def start(self):
        self.ui = uic.loadUi('Calculator.ui')
        self.ui.show()

    def set(self):
        # ------------------------------------------------ Digits ------------------------------------------------------
        self.ui.btn_0.clicked.connect(lambda: self.click(sign=0))
        self.ui.btn_1.clicked.connect(lambda: self.click(sign=1))
        self.ui.btn_2.clicked.connect(lambda: self.click(sign=2))
        self.ui.btn_3.clicked.connect(lambda: self.click(sign=3))
        self.ui.btn_4.clicked.connect(lambda: self.click(sign=4))
        self.ui.btn_5.clicked.connect(lambda: self.click(sign=5))
        self.ui.btn_6.clicked.connect(lambda: self.click(sign=6))
        self.ui.btn_7.clicked.connect(lambda: self.click(sign=7))
        self.ui.btn_8.clicked.connect(lambda: self.click(sign=8))
        self.ui.btn_9.clicked.connect(lambda: self.click(sign=9))
        # ----------------------------------------------- Commands -----------------------------------------------------
        self.ui.btn_c.clicked.connect(lambda: self.click(sign='c'))
        self.ui.btn_com.clicked.connect(lambda: self.click(sign='com'))
        self.ui.btn_div.clicked.connect(lambda: self.click(sign='/'))
        self.ui.btn_eq.clicked.connect(lambda: self.click(sign='eq'))
        self.ui.btn_minus.clicked.connect(lambda: self.click(sign='-'))
        self.ui.btn_mul.clicked.connect(lambda: self.click(sign='*'))
        self.ui.btn_plus.clicked.connect(lambda: self.click(sign='+'))
        self.ui.btn_sign.clicked.connect(lambda: self.click(sign='sign'))
        self.ui.btn_sq.clicked.connect(lambda: self.click(sign='sq'))
        self.ui.btn_sqrt.clicked.connect(lambda: self.click('sqrt'))

    # ----------------------------------------------- Buttons handler --------------------------------------------------
    def click(self, sign):
        # ----------------------------------------------- Digits handler -----------------------------------------------
        if sign in range(10):

            if self.op_result == self.f_num and self.op_sign == '':
                self.click('c')

            if self.op_sign == '':
                if sign == 0 and self.f_num == '' or sign == 0 and self.f_num == '-':
                    self.f_num += '0.'
                elif self.f_num != '':
                    self.f_num += str(sign)
                elif self.f_num == '' and sign != 0:
                    self.f_num += str(sign)
            elif self.op_sign != '':
                if sign == 0 and self.s_num == '' or sign == 0 and self.s_num == '-':
                    self.s_num += '0.'
                elif self.s_num != '':
                    self.s_num += str(sign)
                elif self.s_num == '' and sign != 0:
                    self.s_num += str(sign)
        # ------------------------------------------- '+-/*' buttons handler -------------------------------------------
        elif sign in '+-/*':
            if self.f_num != '' and self.s_num == '':
                self.op_sign = sign
            elif self.s_num != '' and sign in ('sq', 'sqrt'):
                self.operation()
                self.op_sign = sign
                self.operation()
            elif self.s_num != '':
                self.operation()
                self.op_sign = sign
        # -------------------------------------------- Comma button handler --------------------------------------------
        elif sign == 'com':
            if self.f_num != '' and self.op_sign == '' and '.' not in self.f_num:
                if self.f_num == '-':
                    self.f_num += '0.'
                else:
                    self.f_num += '.'
            elif self.f_num != '' and self.op_sign != '' and self.s_num != '' and '.' not in self.s_num:
                if self.s_num == '-':
                    self.s_num += '0.'
                else:
                    self.s_num += '.'
            elif self.f_num == '':
                self.f_num += '0.'
            elif self.f_num != '' and self.op_sign != '' and self.s_num == '':
                self.s_num += '0.'
        # ------------------------------------------ Sign(+/-) button handler ------------------------------------------
        elif sign == 'sign':
            if self.f_num != '' and self.op_sign == '':
                if self.f_num[0] != '-':
                    self.f_num = '-' + self.f_num
                else:
                    self.f_num = self.f_num[1:]
            elif self.f_num == '':
                self.f_num += '-'
            elif self.op_sign != '' and self.s_num != '':
                if '-' not in self.s_num:
                    self.s_num = '-' + self.s_num + ''
                else:
                    self.s_num = self.s_num[1:]
            elif self.s_num == '':
                self.s_num += '-'
        # -------------------------------------------- Clear button handler --------------------------------------------
        elif sign == 'c':
            self.f_num = ''
            self.s_num = ''
            self.op_sign = ''
            self.ui.l_display.setText('0')
        # ----------------------------------- Square and Square Root buttons handler -----------------------------------
        elif sign == 'sq':
            if self.s_num == '' and self.f_num != '' and self.op_sign == '':
                self.op_sign = sign
                self.operation()
            else:
                pass
        elif sign == 'sqrt':
            if self.s_num == '' and self.f_num != '' and self.op_sign == '':
                self.op_sign = sign
                self.operation()
        # -------------------------------------------- Equal button handler --------------------------------------------
        elif sign == 'eq':
            if self.f_num != '' and self.op_sign != '' and self.s_num != '':
                self.operation()
        else:
            self.click('c')

        if sign != 'c':
            self.display()

    # ------------------------------------------------ Label Display ---------------------------------------------------
    def display(self):
        obj = self.ui.l_display

        if self.f_num == '':
            text = '0'
        elif self.s_num != '' and self.s_num[0] == '-':
            text = f'{self.f_num}{self.op_sign}({self.s_num})'
        else:
            text = f'{self.f_num}{self.op_sign}{self.s_num}'

        obj.setText(text)

        if self.f_num == 'ERROR':
            self.f_num = ''
            self.op_result = ''

    # ------------------------------------------------- Calculations ---------------------------------------------------
    def operation(self):
        if self.op_sign == '+':
            self.op_result = float(self.f_num) + float(self.s_num)
        elif self.op_sign == '-':
            self.op_result = float(self.f_num) - float(self.s_num)
        elif self.op_sign == '*':
            self.op_result = float(self.f_num) * float(self.s_num)
        elif self.op_sign == '/':
            if float(self.s_num) == 0:
                self.op_result = 'ERROR'
            else:
                self.op_result = float(self.f_num) / float(self.s_num)
        elif self.op_sign == 'sq':
            self.op_result = float(self.f_num) ** 2
        elif self.op_sign == 'sqrt':
            try:
                self.op_result = math.sqrt(float(self.f_num))
            except Exception:
                self.click('c')
                self.op_result = 'ERROR'
        else:
            self.op_result = 'ERROR'

        if self.op_result != 'ERROR':
            self.op_result = re.sub(r'\.0$', '', str(self.op_result))

        self.f_num = self.op_result
        self.s_num = ''
        self.op_sign = ''


# ------------------------------------------------------- Main ---------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
