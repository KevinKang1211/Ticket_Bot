#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord

from Ticket import ticketPrice, ticketTime

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

    if "<@!{}> ".format(client.user.id) in message.content: #代表有人叫這個bot - bot的id(client.user.id)
        
        if message.author == client.user:
            return
        
        if 'test' in message.content:
            response = "Send message."
            await message.channel.send(response)
    
        elif "Help!" in message.content:
            response = '你需要什麼幫忙?'
            await message.channel.send(response)
        
        else:
            #抓Ticket.py裡面import的function 
            #message.content = 使用者輸入
            response = ticketPrice(message.content)
            response = ticketTime(message.content)
            await message.channel.send(response)
            
    elif "bot 點名" in message.content:
        response = "早安"
        await message.channel.send(response)
    
    else:
        pass
        
client.run(DISCORD_TOKEN)
