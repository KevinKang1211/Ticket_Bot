#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

from THRS import *
import requests
import time
import datetime
dt = datetime.datetime

try:
    from intent import Loki_Departure
    from intent import Loki_Adult
    from intent import Loki_Children
    from intent import Loki_Departure_Time
    from intent import Loki_Destination
    from intent import Loki_Destination_Time
except:
    from .intent import Loki_Departure
    from .intent import Loki_Adult
    from .intent import Loki_Children
    from .intent import Loki_Departure_Time
    from .intent import Loki_Destination
    from .intent import Loki_Destination_Time

from ArticutAPI import ArticutAPI
articut = ArticutAPI.Articut()

LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = "kevink861211@gmail.com"
LOKI_KEY = "msXV9AIraukXeQKbM^*$+3AaU%7eUqC"
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []

        try:
            result = requests.post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": INTENT_FILTER
            })

            if result.status_code == requests.codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # Departure
                if lokiRst.getIntent(index, resultIndex) == "Departure":
                    resultDICT = Loki_Departure.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Adult
                if lokiRst.getIntent(index, resultIndex) == "Adult":
                    resultDICT = Loki_Adult.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Children
                if lokiRst.getIntent(index, resultIndex) == "Children":
                    resultDICT = Loki_Children.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Departure_Time
                if lokiRst.getIntent(index, resultIndex) == "Departure_Time":
                    resultDICT = Loki_Departure_Time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Destination
                if lokiRst.getIntent(index, resultIndex) == "Destination":
                    resultDICT = Loki_Destination.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Destination_Time
                if lokiRst.getIntent(index, resultIndex) == "Destination_Time":
                    resultDICT = Loki_Destination_Time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def amountSTRConvert(inputSTR):
    resultDICT={}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT['number']

#1/22新增  
def ticketTime(message):
    curl = "curl"
    if CURL_PATH != "":
        curl = CURL_PATH    
   
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    departure = "台北" #先寫死
    train_date = dt.now().strftime('%Y-%m-%d') #只取符合API的年月日 ex.2020-1-22 
    time = resultDICT['time']
    dtMessageTime = dt.strptime(time, "%H:%M") #取幾時幾分
    destination = resultDICT['Destination']
    destinationID = getTrainStation(curl, destination)
    departureID = getTrainStation(curl, departure)
    result = getTrainStationStartEnd(curl, departureID, destinationID, train_date)
    
    response=list()
    for train in result:
        dtScheduleTime = dt.strptime(train['OriginStopTime']['DepartureTime'], "%H:%M") #一層一層抓API中JSON檔的value，比較時間並指定時間格式
        if(dtScheduleTime > dtMessageTime):
            response.append(train['OriginStopTime']['DepartureTime'])
            continue
    response.sort() #照順序排
    return "以下是您指定時間可搭乘最接近的班次時間:{}".format(response[0])

def ticketPrice(message): #計算票價
    # curl = "curl"
    # if CURL_PATH != "":
    #     curl = CURL_PATH
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    adultAmount = int(resultDICT['adultAmount'])
    childrenAmount = int(resultDICT['childrenAmount'])
    totalPrice = 1490*adultAmount + 745*childrenAmount
    return "從台北到左營的票價為{}元".format(totalPrice)


if __name__ == "__main__":
    #inputLIST = ["七點半出發的票"]
    # inputLIST = [input("請問您要幾點到哪裡？")]
    # resultDICT = runLoki(inputLIST)
    # print(resultDICT)
    # print("Result => {}".format(resultDICT))
    # print("好的，這邊是您{}點{}分的車票一張，請由1號月台上車，謝謝。".format(resultDICT['hour'], resultDICT['minute']))
    '''
     設定問答必須要有：人數+票價(年齡?)、地點(起+訖)、時間、(@ - 車種、車次)
    →「幾」張票待人數input之後format(大/小或大+小)→ 「幾點幾分」由「哪裡」往「哪裡」的票共「幾張(不同人數)」，「票價」多少。
     '''
    # inputLIST = ["三十分出發的高鐵"]
    # resultDICT = runLoki(inputLIST)
    # #time = amountSTRConvert(resultDICT['time'])
    # print("Result => {}".format(resultDICT))
    # result = getTrainStationStartEnd(curl, "0990", "1070", "2021-01-01")
    # print(result)


    # print(ticketTime("我要一張九點半出發的票"))
    # print(ticketTime('七點四十六分台南到台中的票一張')) #目前都寫死起點是"台北"
    # print(ticketPrice('五大兩小'))
