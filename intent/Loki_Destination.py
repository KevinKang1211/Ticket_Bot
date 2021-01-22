#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Destination

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Destination = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Destination:
        print("[Destination] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "7:46台北到[台南]的票[一張]":
        # write your code here
        resultDICT["Destination"]=args[0]
        pass

    if utterance == "[七點][四十六]分台北到[台南]的票[一張]":
        # write your code here
        resultDICT["Destination"]=args[2]
        pass

    if utterance == "到[台北]":
        # write your code here
        resultDICT["Destination"]=args[0]
        pass

    if utterance == "到[台北]的票[一張]":
        # write your code here
        resultDICT["Destination"]=args[0]
        pass

    if utterance == "往[台北]":
        # write your code here
        resultDICT["Destination"]=args[0]
        pass

    if utterance == "我要[一張]到[台北]的票":
        # write your code here
        resultDICT["Destination"]=args[1]
        pass

    if utterance == "我要到[台北]":
        # write your code here
        resultDICT["Destination"]=args[0]
        pass

    if utterance == "我要去[台北車站]":
        # write your code here
        resultDICT["Destination"]=args[0]
        pass

    if utterance == "我要買從台北到[台南]的車票":
        # write your code here
        resultDICT["Destination"]=args[0]
        pass

    return resultDICT