#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord

from Ticket import ticketPrice, ticketTime

# from Ticket import ticket
#(舊的)將ticket這個function從Ticket.py輸入


DISCORD_TOKEN="Nzg5Mzc0OTIyMzg3NzUwOTc0.X9xIrw.T5UNAinlV0acZTiKD4n7HeBptUA"
DISCORD_GUILD="Droidtown Linguistics Tech."
BOT_NAME = "TicketBot"

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
