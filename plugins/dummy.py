# -*- coding:utf-8 -*-
crontable = []
outputs = []


def process_message(data):
    print("---------- incomming: ----------")
    print(data)
    print("--------------------------------")
    outputs.append((data["channel"], "`*dummy*`"))
