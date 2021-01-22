#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Children

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Children = True
userDefinedDICT = {"大": ["大人", "成人"], "小": ["小孩", "孩童"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Children:
        print("[Children] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[三]大[一]小":
        # write your code here
        resultDICT["Children"]=args[1]
        pass

    if utterance == "[三個]大人[兩個]小孩":
        # write your code here
        resultDICT["Children"]=args[1]
        pass

    if utterance == "[三個]小孩":
        # write your code here
        resultDICT["Children"]=args[0]
        pass

    if utterance == "[三個]小孩[兩個]大人":
        # write your code here
        resultDICT["Children"]=args[0]
        pass

    return resultDICT