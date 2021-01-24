#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
import json

# Widnows 須下載 curl 套件
# https://curl.haxx.se/windows/
#CURL_PATH = "D:\Applications\curl\curl-7.67.0-win64-mingw\bin\curl.exe"    # Windows 範例
CURL_PATH = ""  # MacOSX / Linux 留空

stationDICT=[
            {'stationName': '南港', 'stationID': '0990'},
            {'stationName': '台北', 'stationID': '1000'},
            {'stationName': '板橋', 'stationID': '1010'},
            {'stationName': '桃園', 'stationID': '1020'},
            {'stationName': '新竹', 'stationID': '1030'},
            {'stationName': '苗栗', 'stationID': '1035'},
            {'stationName': '台中', 'stationID': '1040'},
            {'stationName': '彰化', 'stationID': '1043'},
            {'stationName': '雲林', 'stationID': '1047'},
            {'stationName': '嘉義', 'stationID': '1050'},
            {'stationName': '台南', 'stationID': '1060'},
            {'stationName': '左營', 'stationID': '1070'},
            ]

def getCurl(curl, url):
    # curl
    resultSTR = subprocess.check_output([curl, "-X", "GET", url]).decode("utf-8")
    resultDICT = json.loads(resultSTR, encoding="utf-8")
    return resultDICT

def getTrainDate(curl, date):
    """
    GET /v2/Rail/THSR/DailyTrainInfo/TrainDate/{TrainDate}
    取得指定[日期]所有車次的車次資料
    """
    trainDateUrl = "https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTrainInfo/TrainDate/{}?$top=30&$format=JSON".format(date)
    resultDICT = getCurl(curl, trainDateUrl)
    return resultDICT

def getTrainNo(curl, date, no):
    """
    GET /v2/Rail/THSR/DailyTrainInfo/TrainNo/{TrainNo}/TrainDate/{TrainDate}
    取得指定[日期],[車次]的車次資料
    """
    trainDateUrl = "https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTrainInfo/TrainNo/{}/TrainDate/{}?$top=30&$format=JSON".format(no, date)
    resultDICT = getCurl(curl, trainDateUrl)
    return resultDICT

def getTrainStationStartEnd(curl, departure, destination, date):
    """
    GET /v2/Rail/THSR/DailyTimetable/OD/{OriginStationID}/to/{DestinationStationID}/{TrainDate}
    取得指定[日期],[起迄站間]之時刻表資料

    *Milan寫的function, 對應API必填的參數
    """
    trainStationTimeUrl = "https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable/OD/{}/to/{}/{}?$top=30&$format=JSON".format(departure, destination, date)
    resultDICT = getCurl(curl, trainStationTimeUrl)
    return resultDICT


if __name__ == "__main__":
    # curl 路徑
    curl = "curl"
    if CURL_PATH != "":
        curl = CURL_PATH

    # 日期 格式: yyyy-mm-dd
    date = "2021-01-13"
    # 車次 格式: ####
    no   = "0657"

    #1/22新增: 先寫死起訖站   
    departureStation = "南港"
    destinationStation = "嘉義"


    # 取得指定日期車次資料
    with open("THRS_date.json", "w", encoding="utf-8") as f:
        result = getTrainDate(curl, date)
        json.dump(result, f, ensure_ascii=False)

    # 取得指定日期和車次資料
    with open("THRS_date_no.json", "w", encoding="utf-8") as f:
        result = getTrainNo(curl, date, no)
        json.dump(result, f, ensure_ascii=False)

    
    ### Milan 1/22新增

    #取得車站ID -> 可以使用到[時間][起迄]的函式
    with open("THRS_station.json", "w", encoding="utf-8") as f:
        result = getTrainStation(curl, departureStation)
        json.dump(result, f, ensure_ascii=False)

    #取得指定時間和起訖車站
    with open("THRS_station_start_end", "w", encoding = "utf-8") as f:
        departureID = getTrainStation(curl, departureStation)
        destinationID = getTrainStation(curl, destinationStation)
        result = getTrainStationStartEnd(curl, departureID, destinationID, date)
        json.dump(result, f, ensure_ascii=False)