#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Departure_Time

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Departure_Time = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

from ArticutAPI import ArticutAPI
articut = ArticutAPI.Articut()

#為了處理API時間的格式，用datetime的套件
from datetime import datetime
dt = datetime.now()

#為了轉換數字；對應articut lv3切出來的dict(i.e. {time})
def amountSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT

#新增一個function只抓取articut output的number dict (為了做時間的處理)
def numberSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT['number']


# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Departure_Time:
        print("[Departure_Time] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[7]:[46]台北到台南的票[一張]":
        # resultDICT['hour'] = args[0]
        # resultDICT['minute'] = args[1]
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[0]+":"+args[1]
        pass

    if utterance == "[9]:[30]出發的票[一張]":
        # resultDICT['hour'] = args[0]
        # resultDICT['minute'] = args[1]
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[0]+":"+args[1]
        pass

    if utterance == "[七點][四十六]分台北到台南的票[一張]":
        # time = amountSTRConvert(args[0]+args[1])["time"] #讓[七點]、[四十六]合併list內容後(=七點四十六)丟進articut lv3作轉換(會得到input, entity...等等dictionary)，選擇'time'這個dict並存進time這個變數 → *如同直接在articut網站打七點四十六分 
        # resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]  #繼續觀察lv3的'time'這個dict最外層有兩個list，故time[0][0]→再來取"timespan"這個key裡面包的"hour"，這個key的value中第一個index
        # resultDICT['minute'] = time[0][0]["time_span"]["minute"][0] #同理'hour'的作法。 
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['ticketAmount'] = args[2][0]                #計算票的張數
        resultDICT['date'] = datetime[0][0]["datetime"][0:10] #抓articutAPI中time的日期（前十格）
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3] #抓articutAPI中time的時間（後八格）
        pass

    if utterance == "[三十分]出發的高鐵":
        # time = amountSTRConvert(args[0])["time"] 
        # resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        
        hour = dt.strftime("%H")                                #因為沒有提到「時」，故把輸入當下的時用套件提出來
        minute = numberSTRConvert(args[0][0:2])[args[0][0:2]]
        resultDICT['time'] = "{}:{}".format(hour, minute)       #合併上兩行結果
    
        resultDICT['date'] = dt.strftime('%Y-%m-%d') #此行抓出日期並format(年月日)
        resultDICT['destination'] = "左營"           #沒說目的地的都先寫死給左營
        pass

    if utterance == "[九點][半]出發的票":
        # time = amountSTRConvert(args[0]+args[1])["time"] #9:30
        # resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        # resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        resultDICT['ticketAmount'] = 1
        datetime = amountSTRConvert(args[0]+args[1])["time"]
        resultDICT['datetime'] = datetime[0][0]["datetime"]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:]
        resultDICT['destination'] = "左營"
        pass

    if utterance == "我要[一張][7]:[46]到台南的票":
        # resultDICT['hour'] = args[1]
        # resultDICT['minute'] = args[2]
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[1]+":"+args[2]
        pass

    if utterance == "我要[一張][9]:[30]出發的票":
        # resultDICT['hour'] = args[1]
        # resultDICT['minute'] = args[2]
        resultDICT['date'] = dt.strftime('%Y-%m-%d')
        resultDICT['time'] = args[1]+":"+args[2]
        resultDICT['destination'] = "左營"
        pass

    if utterance == "我要[一張][七點][四十六]分到台南的票":
        # time = amountSTRConvert(args[1]+args[2])["time"]
        # resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        # resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        datetime = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['hour'] = datetime[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = datetime[0][0]["time_span"]["minute"][0]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:-3]
        resultDICT['ticketAmount'] = args[0][0]
        pass

    if utterance == "我要[一張][九點][半]出發的票":
        # time = amountSTRConvert(args[1]+args[2])["time"]
        # resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        # resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        datetime = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['hour'] = datetime[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = datetime[0][0]["time_span"]["minute"][0]
        resultDICT['date'] = datetime[0][0]["datetime"][0:10]
        resultDICT['time'] = datetime[0][0]["datetime"][-8:]
        resultDICT['ticketAmount'] = args[0][0]
        resultDICT['destination'] = "左營"
        pass

    return resultDICT