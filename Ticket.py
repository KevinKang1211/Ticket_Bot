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
from ArticutAPI import ArticutAPI
articut = ArticutAPI.Articut()
import datetime
dt = datetime.datetime
import json
import logging
from ref_data import stationLIST, animalLIST, TaiwanLIST
from requests import post
from requests import codes
import math

try:
    from intent import Loki_query_time
    from intent import Loki_Adult
    from intent import Loki_Destination
    from intent import Loki_Children
    from intent import Loki_Departure
    from intent import Loki_Destination_Time
    from intent import Loki_Departure_Time
except:
    from .intent import Loki_query_time
    from .intent import Loki_Adult
    from .intent import Loki_Destination
    from .intent import Loki_Children
    from .intent import Loki_Departure
    from .intent import Loki_Destination_Time
    from .intent import Loki_Departure_Time


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = ""
LOKI_KEY = ""
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

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
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

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # query_time
                if lokiRst.getIntent(index, resultIndex) == "query_time":
                    resultDICT = Loki_query_time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Adult
                if lokiRst.getIntent(index, resultIndex) == "Adult":
                    resultDICT = Loki_Adult.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Destination
                if lokiRst.getIntent(index, resultIndex) == "Destination":
                    resultDICT = Loki_Destination.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Children
                if lokiRst.getIntent(index, resultIndex) == "Children":
                    resultDICT = Loki_Children.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Departure
                if lokiRst.getIntent(index, resultIndex) == "Departure":
                    resultDICT = Loki_Departure.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Destination_Time
                if lokiRst.getIntent(index, resultIndex) == "Destination_Time":
                    resultDICT = Loki_Destination_Time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Departure_Time
                if lokiRst.getIntent(index, resultIndex) == "Departure_Time":
                    resultDICT = Loki_Departure_Time.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)

#Self-Defined

def loadJson(filename):
    with open(filename,"r") as f:
        result = json.load(f)
    return result

def ticketTime(message): 
    inputLIST = [message]
    resultDICT = runLoki(inputLIST)
    print(resultDICT)
    departure = resultDICT['departure'] #str
    destination = resultDICT['destination'] #str
    if 'departure_time' in resultDICT:
        logging.debug('departure time in resultDICT')
        time = resultDICT['departure_time']
    elif 'destination_time' in resultDICT:
        logging.debug('destination time in resultDICT')
        time = resultDICT['destination_time'] #check if the time is correctly put in resultDICT
    else:
        logging.debug('Take the present time')
        time = dt.now().strftime('%H:%M')
    dtMessageTime = dt.strptime(time, "%H:%M") #datetime object
    departureTimeList=list()
    timeTable = loadJson("THRS_timetable.json") #DICT
    for station in stationLIST:
        if departure == station['stationName']:
            logging.debug('Departure sequence = 0 recorded')
            departureSeq = station['stationSeq'] #Normally departureSequence & destinationSeq will be object of integer
        if destination == station['stationName']:
            logging.debug('destination sequence recorded')
            destinationSeq = station['stationSeq']
    if departureSeq < destinationSeq: 
        # check if it's going north or south. 
        # While departureSeq < destinationSeq, then it's going south.
        direction = 0
        for trainSchedule in timeTable:
            if direction == trainSchedule['GeneralTimetable']['GeneralTrainInfo']['Direction']: # Check json
                logging.debug('direction checked')
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        logging.debug('departure name checked')
                        if 'DepartureTime' in trainStop:
                            dtDepartureTime = dt.strptime(trainStop['DepartureTime'], "%H:%M")
                            if dtDepartureTime > dtMessageTime:
                                departureTime = dt.strftime(dtDepartureTime, "%H:%M")
                                departureTimeList.append(departureTime) 
    if departureSeq > destinationSeq:
        # While departureSeq < destinationSeq, then it's going south.
        direction = 1
        for trainSchedule in timeTable:
            if direction == trainSchedule['GeneralTimetable']['GeneralTrainInfo']['Direction']: #check json
                logging.debug('direction = 1 checked')
                for trainStop in trainSchedule['GeneralTimetable']['StopTimes']:
                    if departure == trainStop['StationName']['Zh_tw']:
                        logging.debug('destination name checked')
                        if 'DepartureTime' in trainStop:
                            dtDepartureTime = dt.strptime(trainStop['DepartureTime'], "%H:%M")
                            if dtDepartureTime > dtMessageTime:
                                resultTime = dt.strftime(dtDepartureTime, "%H:%M")
                                departureTimeList.append(resultTime)                            
    departureTimeList.sort()
    return "以下是您指定時間可搭乘最接近的班次時間： {}".format(departureTimeList[0])



if __name__ == "__main__":
    # # query_time
    # print("[TEST] query_time")
    # inputLIST = ['19:47','19：15']
    # testLoki(inputLIST, ['query_time'])
    # print("")

    # # Adult
    # print("[TEST] Adult")
    # inputLIST = ['兩大','三個大人','三大一小','三小一大','兩張全票','兩張成人票','三個大人兩個小孩','三個小孩兩個大人']
    # testLoki(inputLIST, ['Adult'])
    # print("")

    # # Destination
    # print("[TEST] Destination")
    # inputLIST = ['到台北','去台北','往台北']
    # testLoki(inputLIST, ['Destination'])
    # print("")

    # # Children
    # print("[TEST] Children")
    # inputLIST = ['三個小孩','三大一小','三小一大','兩張優待票','兩張兒童票','兩張孩童票','三個大人兩個小孩','三個小孩兩個大人']
    # testLoki(inputLIST, ['Children'])
    # print("")

    # # Departure
    # print("[TEST] Departure")
    # inputLIST = ['從台北','台北出發','台北去台南','新竹到台北','新竹往台北','從台北到台南','從台北去台南','從台北往台南']
    # testLoki(inputLIST, ['Departure'])
    # print("")

    # # Destination_Time
    # print("[TEST] Destination_Time")
    # inputLIST = ['九點半以前到台南的票','我要一張9:30以前到台南的票']
    # testLoki(inputLIST, ['Destination_Time'])
    # print("")

    # # Departure_Time
    # print("[TEST] Departure_Time")
    # inputLIST = ['9:30出發','三十分出發','九點半出發','下午三點之後','五十分到台南','早上九點之前','早上八點出發','7:46台北到台南','9:54從台北到台南','下午三點五十之後','七點四十六分往台南','五十分從台北到台中','十一點從台北到台中','早上九點四十分之前','早上八點三十分出發','下午三點五十分到台南','早上五點半台北到左營','七點四十六分台北往台南','五點五十分從台北到台中']
    # testLoki(inputLIST, ['Departure_Time'])
    # print("")

    # 輸入其它句子試看看
    inputLIST = ["五點左右台北到左營"]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    #print("Result => {}".format(resultDICT))