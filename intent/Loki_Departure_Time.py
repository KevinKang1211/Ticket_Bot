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

#為了轉換數字；對應articut lv3切出來的dict(i.e. {time})
def amountSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT


# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Departure_Time:
        print("[Departure_Time] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[7]:[46]台北到台南的票[一張]":
        # write your code here
        resultDICT['hour'] = args[0]
        resultDICT['minute'] = args[1]
        pass

    if utterance == "[9]:[30]出發的票[一張]":
        # write your code here
        resultDICT['hour'] = args[0]
        resultDICT['minute'] = args[1]
        pass

    if utterance == "[七點][四十六]分台北到台南的票[一張]":
        # write your code here
        time = amountSTRConvert(args[0]+args[1])["time"] 
#讓[七點]、[四十六]合併list內容後(=七點四十六)丟進articut lv3作轉換(會得到input, entity...等等dictionary)，選擇'time'這個dict並存進time這個變數 → *如同直接在articut網站打七點四十六分
        resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]  
#繼續觀察lv3的'time'這個dict最外層有兩個list，故time[0][0]→再來取"timespan"這個key裡面包的"hour"，這個key的value中第一個index
        resultDICT['minute'] = time[0][0]["time_span"]["minute"][0] #同理'hour'的作法。 
        
####*搞清楚這一包的結構(dict混list的寫法，問Keith)
        pass

    if utterance == "[三十分]出發的高鐵":
        # write your code here
        time = amountSTRConvert(args[0])["time"] 
        resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        pass

    if utterance == "[九點][半]出發的票":
        # write your code here
        time = amountSTRConvert(args[0]+args[1])["time"] #9:30
        resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        pass

    if utterance == "我要[一張][7]:[46]到台南的票":
        # write your code here
        resultDICT['hour'] = args[1]
        resultDICT['minute'] = args[2]
        pass

    if utterance == "我要[一張][9]:[30]出發的票":
        # write your code here
        resultDICT['hour'] = args[1]
        resultDICT['minute'] = args[2]
        pass

    if utterance == "我要[一張][七點][四十六]分到台南的票":
        # write your code here
        time = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        pass

    if utterance == "我要[一張][九點][半]出發的票":
        # write your code here
        time = amountSTRConvert(args[1]+args[2])["time"]
        resultDICT['hour'] = time[0][0]["time_span"]["hour"][0]
        resultDICT['minute'] = time[0][0]["time_span"]["minute"][0]
        pass

    return resultDICT