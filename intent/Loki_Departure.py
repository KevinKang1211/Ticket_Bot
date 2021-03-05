#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Departure

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Departure = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Departure:
        print("[Departure] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[台北]出發":
        resultDICT['departure'] = args[0]
        pass

    if utterance == "[台北]去台南":
        resultDICT['departure'] = args[0]
        pass
    
    if utterance == "[新竹]往台北": #手動新增, Loki下載時沒有顯示，但使用測試工具有分別
        resultDICT['departure'] = args[0]
        pass

    if utterance == "[新竹]到台北": #手動新增
        resultDICT['departure'] = args[0]
        pass

    if utterance == "從[台北]":
        if "從{}".format(args[0]) in inputSTR:
            resultDICT['departure'] = args[0]
        pass

    if utterance == "從[台北]到台南":
        if "從{}".format(args[0]) in inputSTR:
            resultDICT['departure'] = args[0]
        pass

    if utterance == "從[台北]往台南":
        if "從{}".format(args[0]) in inputSTR:
            resultDICT['departure'] = args[0]
        pass

    return resultDICT