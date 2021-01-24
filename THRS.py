#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
import json

# Widnows 須下載 curl 套件
# https://curl.haxx.se/windows/
#CURL_PATH = "D:\Applications\curl\curl-7.67.0-win64-mingw\bin\curl.exe"    # Windows 範例
CURL_PATH = ""  # MacOSX / Linux 留空

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


if __name__ == "__main__":
    # curl 路徑
    curl = "curl"
    if CURL_PATH != "":
        curl = CURL_PATH

    # 日期 格式: yyyy-mm-dd
    date = "2021-01-13"
    # 車次 格式: ####
    no   = "0657"

    # 取得指定日期車次資料
    with open("THRS_date.json", "w", encoding="utf-8") as f:
        result = getTrainDate(curl, date)
        json.dump(result, f, ensure_ascii=False)

    # 取得指定日期和車次資料
    with open("THRS_date_no.json", "w", encoding="utf-8") as f:
        result = getTrainNo(curl, date, no)
        json.dump(result, f, ensure_ascii=False)
    #print(result)