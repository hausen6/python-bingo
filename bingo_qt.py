#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from threading import Thread
from subprocess import call
from time import sleep
from random import shuffle

from PyQt4 import QtCore, QtGui, Qt


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.last_number = list(range(1, 76))
        self.selected_number = []

        # gui
        # lavel
        self.label = QtGui.QLabel("Bingo Start!!!", self)
        self.font = QtGui.QFont("Helvetica", 200)
        self.label.setFont(self.font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # Bottun
        self.btn = QtGui.QPushButton("Next Number", self)
        self.btn.clicked.connect(self.numberProduce)

        # layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label, 0)
        layout.addWidget(self.btn, 1)
        self.setLayout(layout)

    def numberProduce(self, ):
        """
        番号を選ぶ演出をする
        """
        call("clear")
        numbers = list(range(1, 76))
        shuffle(numbers)

        rate = 75
        timer = QtCore.QTimer()
        timer.setInterval(1. / rate * 1000)

        def produce():
            nonlocal rate
            try:
                number = numbers.pop(0)
            except (IndexError):
                # 数の引き終わり
                timer.stop()
                return self.selectNumber()
            self.label.setText("{0:2d}".format(number))
            print("\007")
            _time = 1. / rate * 1000 * 1.1
            rate -= 1
            timer.setInterval(_time)

        timer.timeout.connect(produce)
        timer.start()

    def windowTwincle(self, ):
        timer = QtCore.QTimer()
        timer.setInterval(500)
        num_twincle = 10

        def twincle():
            nonlocal num_twincle
            palette = self.label.palette()
            if num_twincle % 2 == 0:
                color = QtGui.QColor("red")
            else:
                color = QtGui.QColor("yellow")
            if num_twincle == 0:
                color = QtGui.QColor(QtCore.Qt.white)
                timer.stop()

            self.label.setAutoFillBackground(True)
            palette.setColor(self.label.backgroundRole(), color)
            self.label.setPalette(palette)
            num_twincle -= 1

        timer.timeout.connect(twincle)
        timer.start()

    def selectNumber(self, ):
        # 番号をシャッフル
        shuffle(self.last_number)

        # 番号を選択
        try:
            number = self.last_number.pop(0)
        except (IndexError):
            self.label.setText("Finish BINGO!!!\nThank you for playing!!!")
            return
        else:
            self.selected_number.append(number)
            self.label.setText("{0:2d}".format(number))

        # ビンゴ情報をコンソールに出力
        call("clear")
        print("Selected Numbers: ")
        for i, num in enumerate(self.selected_number, 1):
            print(num, end="\t")
            if (i % 5 == 0) and i > 0:
                print()
        print()
        print("=" * 30)
        print("Last Numbers: ")
        for i, num in enumerate(sorted(self.last_number), 1):
            print(num, end="\t")
            if (i % 5 == 0) and i > 0:
                print()
        print()
        say = Thread(target=self.say_number, args=(number, ))
        say.start()
        self.windowTwincle()

    def say_number(self, number):
        call(["say", "-v", "Zarvox", "{}".format(number)])

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()

    win = MainWindow(main_window)
    main_window.setCentralWidget(win)
    main_window.show()
    app.exec_()
