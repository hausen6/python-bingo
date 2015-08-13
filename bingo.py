#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import sys
from subprocess import call
from random import shuffle
import tkinter as tk


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.last_number = list(range(1, 76))  # 1 ~ 75 がbingoの番号
        self.selected_number = []  # 選択された番号

        # gui
        self.current_number_label = tk.Label(self, text="Bingo Start!!!", font=("Helvetica", 180), width=10)
        self.btn = tk.Button(self, text="Next", command=self.selectProduce)

        # layout
        self.btn.pack(side=tk.TOP, expand=True, fill="both")
        self.current_number_label.pack(side=tk.TOP, expand=True, fill="both", )

    def selectProduce(self, ):
        """
        選んでいるっぽい演出をする
        """
        produced_number = list(range(1, 76))
        shuffle(produced_number)

        def pop(rate):
            try:
                number = produced_number.pop(0)
            except (IndexError):
                self.after_cancel(self.running_id)
                self.selectNumber()
                self.windowTwincle(10)
            else:
                self.current_number_label.configure(text="{0}".format(number), justify="center")
                _time = int((1. / rate) * 1000)
                rate -= 1
                self.running_id = self.after(_time, pop, rate)

        return pop(75)

    def windowTwincle(self, num):
        """
        選んだぞ!!!を表現するためにwindowをチカチカさせる

        Parameters
        ----------
        num: チカチカさせる回数
        """
        if num == 0:
            self.current_number_label.configure(bg="white")
            self.after_cancel(self.running_id)
            return
        if num % 2 == 0:
            self.current_number_label.configure(bg="red")
        else:
            self.current_number_label.configure(bg="yellow")
        num -= 1
        self.running_id = self.after(500, self.windowTwincle, num)

    def selectNumber(self, ):
        """
        番号を選択する関数
        """
        # 番号をシャッフル
        shuffle(self.last_number)

        # 0番目を抜き出す
        try:
            number = self.last_number.pop(0)
        except (IndexError):
            # 全ての番号を抜き出し終わったのでBingo終了
            self.current_number_label.configure(text="Bingo Finish!!!", bg="red")
            return
        else:
            self.selected_number.append(number)

        # 表示を変更
        self.current_number_label.configure(text="{0:d}".format(number), justify="center")

        # コンソールには今まで選ばれた番号を表示
        try:
            self.now_number += 1
        except (NameError, AttributeError):
            self.now_number = 1
        if self.now_number % 5 == 0:
            print()
        print(number, end="\t")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Let's Bingo")

    frame = MainWindow(root)
    frame.pack(expand=True, fill="both")

    # 選択番号の表示
    call("clear", shell=True)
    print("Selected Numbers:")
    print("=" * 30)

    root.mainloop()
