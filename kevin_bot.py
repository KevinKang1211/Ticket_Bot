#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord

#*還沒修改主程式的code: from Ticket import ticket, ticketPrice, runLoki

try:
    with open("./account.info", "r") as f:
        accountDICT = json.loads(f.read())
except:
    accountDICT = {}

class Articut:
    def __init__(self, username="", apikey="", version="latest", level="lv2"):
        '''
        username = ""    # 你註冊時的 email。若留空，則會使用每小時更新 2000 字的公用帳號。
        apikey = ""      # 您完成付費後取得的 apikey 值。若留空，則會使用每小時更新 2000 字的公用帳號。
        '''
        if "articut" in accountDICT:
            self.username = accountDICT["articut"]["username"]
            self.apikey = accountDICT["articut"]["apikey"]
        else:
            self.username = username
            self.apikey = apikey


# Discord New Info
if "discord" in accountDICT:
    DISCORD_TOKEN = accountDICT["discord"]["token"]
    DISCORD_GUILD = accountDICT["discord"]["guild"]
    BOT_NAME = accountDICT["discord"]["name"]
else:
    DISCORD_TOKEN = ""
    DISCORD_GUILD = ""
    BOT_NAME = ""

#設定全域變數
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
#responseDICT = {}
# {"ID": {"1":xxx, "2":xxx, "3":xxx}}


# Documention
# https://discordpy.readthedocs.io/en/latest/api.html#client

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break
    print(f'{BOT_NAME}bot has connected to Discord!')
    print(f'{guild.name}(id:{guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print("message.content", message.content)

    if "<@!{}> ".format(client.user.id) in message.content: #代表有人叫這個bot - bot的id = (client.user.id)
        inputSTR = message.content.replace("<@!{}> ".format(clinet.user.id), "")
        inputLIST = [inputSTR]
        resultDICT = runLoki(inputLIST)
        paxDICT = {}
                #       "ID": 
                #           {   
                #               "time": {"departure_time": "", "destination_time": ""}, 
                #               "station": {"departure": "", "destination": ""},
                #               "adultAmount": 0, 
                #               "childrenAmount": 0
                #           }
                #   }
        if str(message.author.id) not in paxDICT:
            #設定以ID為key, 輸入的所有資訊為value(包成大Dict)
            paxDICT[str(message.author.id)] = {
                "time": ["departure_time": "", "destination_time": ""], 
                "station": ["departure": "", "destination": ""],
                "adultAmount": 0, 
                "childrenAmount": 0
            }

        '''
        1. 上方paxDICT的「起始站」先寫死，現階段會比較好寫? (因兩個和time有關的Intent，args也是寫死「台北」，可以後續再做修改)
        2. Keith範例: y,n的elif部分(我們則是1,2,3)不太清楚需要打在哪才能運作 (那段我問他，當時沒有解釋得很清楚)
        3. 不知道該如何設定一開始就顯示「請輸入代碼選擇功能:」(下方有嘗試寫，但不確定該放在什麼位置)，因為在Discord中我們都是呼叫BOT然後直接輸入文字 
        4. 除了之前Word和你提到，在「僅查詢班次」的選擇中，還想到了這種不易處理的可能句型: xx點「發車/出發」的車 ； xx點「抵達/到」的車
        →  還是這個問題應該在Loki的Intent中解決?

        *將format最後顯示的內容(i.e., 回傳的票價或時間)改在這個檔案寫，而不是寫在主程式的Function裡面。 (想說以你那邊為主所以我還沒動)
        '''
        # 這樣寫不知道可否? (後續縮排需調整?)
        # if str(message.author.id) not in responseDICT: 
        #     responseDICT[str(message.author.id)] = {"1":"請輸入時間與起訖站來查詢班次: ", "2":"請輸入人數與起訖站來查詢票價: ", "3":"請輸入時間、人數、起訖站進行購票: "} #先設定好對應的Value是什麼
        #     await message.channel.send("請輸入代碼選擇服務項目(1:查詢班次/2:查詢票價/3:購票): ")
        #     return
        
        if "1" in message.content: #僅查詢班次 (*需思考沒有完整時間，給現在時間? 還是intent可以解決? 使用者只給出發或抵達時間；給時間段；最早?最晚?→ 補在intent內? )
            inputSTR = message.content.replace("<@!{}> ".format(clinet.user.id), "")
            inputLIST = [inputSTR]
            resultDICT = runLoki(inputLIST)
            if 'departure_time' in resultDICT:
                paxDICT[str(message.author.id)]['time']['departure_time'] = resultDICT['departure_time']
            if 'destination_time' in resultDICT:
                paxDICT[str(message.author.id)]['time']['destination_time'] = resultDICT['destination_time']
            if 'departure' in resultDICT:
                paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
            if 'destination' in resultDICT:
                paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
            
            if paxDICT[str(message.author.id)]['time']['departure_time'] == "":
                await message.channel.response("你沒有打時間啊！想知道幾點以前到請打時間")
                return
            if paxDICT[str(message.author.id)]['time']['destination_time'] =="":
                await message.channel.response("你沒有打時間啊！想知道幾點以前到請打時間")
                return
            if paxDICT[str(message.author.id)]['station']['departure'] =="":
                await message.channel.response("請輸入起點站")
                return
            if paxDICT[str(message.author.id)]['station']['destination'] == "":
                await message.channel.response("請輸入終點站")
            
            #滿足條件後:
            response = ticket(message.content)
            await message.channel.send(response)
            del paxDICT[str(message.author.id)]

        elif "2" in message.content: #僅查詢票價
            inputSTR = message.content.replace("<@!{}> ".format(clinet.user.id), "")
            inputLIST = [inputSTR]
            resultDICT = runLoki(inputLIST)
            if 'departure' in resultDICT:
                paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
            if 'destination' in resultDICT:  
                paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
            if 'adultAmount' in resultDICT:
                paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
            if 'childrenAmount' in resultDICT:
                paxDICT[str(message.author.id)]['childrenDICT'] = resultDICT['childrenAmount']

            if paxDICT[str(message.author.id)]['station']['departure'] =="":
                await message.channel.response("請輸入起點站")
                return
            if paxDICT[str(message.author.id)]['station']['destination'] == "":
                await message.channel.response("請輸入終點站")
                return
            if paxDICT[str(message.author.id)]['adultAmount'] == 0:
                await message.channel.response("麻煩請你輸入有幾位大人")
                return
            if paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                await message.channel.response("麻煩請你輸入有幾位小孩")
                return
            
            #滿足條件後:
            response = ticketPrice(message.content)
            await message.channel.send(response)
            del paxDICT[str(message.author.id)]
        
        elif "3" in message.content: #購票
            inputSTR = message.content.replace("<@!{}> ".format(clinet.user.id), "")
            inputLIST = [inputSTR]
            resultDICT = runLoki(inputLIST)
            if 'departure_time' in resultDICT:
                paxDICT[str(message.author.id)]['time']['departure_time'] = resultDICT['departure_time']
            if 'destination_time' in resultDICT:
                paxDICT[str(message.author.id)]['time']['destination_time'] = resultDICT['destination_time']
            if 'departure' in resultDICT:
                paxDICT[str(message.author.id)]['station']['departure'] = resultDICT['departure']
            if 'destination' in resultDICT:
                paxDICT[str(message.author.id)]['station']['destination'] = resultDICT['destination']
            if 'adultAmount' in resultDICT:
                paxDICT[str(message.author.id)]['adultAmount'] = resultDICT['adultAmount']
            if 'childrenAmount' in resultDICT:
                paxDICT[str(message.author.id)]['childrenDICT'] = resultDICT['childrenAmount']

            if paxDICT[str(message.author.id)]['time']['departure_time'] == "":
                await message.channel.response("你沒有打時間啊！想知道幾點以前到請打時間")
                return
            if paxDICT[str(message.author.id)]['time']['destination_time'] =="":
                await message.channel.response("你沒有打時間啊！想知道幾點以前到請打時間")
                return
            if paxDICT[str(message.author.id)]['station']['departure'] =="":
                await message.channel.response("請輸入起點站")
                return
            if paxDICT[str(message.author.id)]['station']['destination'] == "":
                await message.channel.response("請輸入終點站")
                return

            #如果只有輸入「x張/x人」，可以直接用現有的intent判斷?
            if paxDICT[str(message.author.id)]['adultAmount'] == 0:
                await message.channel.response("請輸入有幾位大人")
                return
            if paxDICT[str(message.author.id)]['childrenAmount'] == 0:
                await message.channel.response("請輸入有幾位小孩")
                return
            
            #滿足條件後:

            respPrice = ticketPrice(message.content)
            respTime  = ticket(message.content)
            #(兩項分開存，下行format顯示的內容可以再調整) 
            #response  = respPrice + ", " + respTime
            await message.channel.send(response)
            del paxDICT[str(message.author.id)]
        else:
            pass
        
        # if message.author == client.user:
        #     return
        # if 'test' in message.content:
        #     response = "Send message."
        #     await message.channel.send(response)    
        # elif "Help!" in message.content:
        #     response = '你需要什麼幫忙?'
        #     await message.channel.send(response)


    elif "bot 點名" in message.content:
        response = "早安"
        await message.channel.send(response)
    
    else:
        pass
        
client.run(DISCORD_TOKEN)
