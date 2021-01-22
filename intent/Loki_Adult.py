#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Adult

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Adult = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Adult:
        print("[Adult] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[三]大[一]小":
        # write your code here
        resultDICT["Adult"]=args[0]
        pass

    if utterance == "[三]小[一]大":
        # write your code here
        resultDICT["Adult"]=args[1]
        pass

    if utterance == "[三個]大人":
        # write your code here
        resultDICT["Adult"]=args[0]
        pass

    if utterance == "[三個]大人[兩個]小孩":
        # write your code here
        resultDICT["Adult"]=args[0]
        pass

    if utterance == "[三個]小孩[兩個]大人":
        # write your code here
        resultDICT["Adult"]=args[1]
        pass

    return resultDICT