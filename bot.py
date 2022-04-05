# bot.py
import os
import requests
import pandas as pd
import numpy as np

import discord
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.environ['DISCORD_TOKEN']

data_start = {}
for name in names_our:
    idd = name["id"]
    price_arr = requests.get(f"https://api.coingecko.com/api/v3/coins/{idd}/history?date=01-04-2022&localization=false").json()
    try:
        data_start[name["id"]] = price_arr["market_data"]["current_price"]["usd"]
    except KeyError:
        data_start[name["id"]] = np.nan

ids = []
for name in names_our:
    ids.append(name["id"])
ids_str = ",".join(ids)

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'L2 Trading Competition precise':
        pd.set_option('display.precision', 6)
        data_now = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd").json()
        df = pd.DataFrame(columns=["project", "1 April", "now", "PnL, %"])
        for name in names_our:
            idd = name["id"]
            cur = pd.DataFrame([[name["name"], data_start[idd], data_now[idd]["usd"], "NaN"]],
                               columns=["project", "1 April", "now", "PnL, %"])
            df = pd.concat([df, cur], ignore_index=True)
        df.loc[:, "PnL, %"] = (df.loc[:, "now"].div(df.loc[:, "1 April"])-1)*100
        df = df.sort_values("PnL, %", ascending=False, ignore_index=True)

        response = '```'+df.to_string()+'```'
        await message.channel.send(response)



    if message.content == 'L2 Trading Competition':
        pd.set_option('display.precision', 4)
        data_now = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd").json()
        df = pd.DataFrame(columns=["project", "1 April", "now", "PnL, %"])
        for name in names_our:
            idd = name["id"]
            cur = pd.DataFrame([[name["name"], data_start[idd], data_now[idd]["usd"], "NaN"]],
                               columns=["project", "1 April", "now", "PnL, %"])
            df = pd.concat([df, cur], ignore_index=True)
        df.loc[:, "PnL, %"] = (df.loc[:, "now"].div(df.loc[:, "1 April"])-1)*100
        df = df.sort_values("PnL, %", ascending=False, ignore_index=True)
        response = '```'+df.to_string()+'```'
        await message.channel.send(response)

    if message.content == 'L2 Trading Competition Grugs':
        pd.set_option('display.precision', 4)
        data_now = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd").json()
        df_grugs = pd.DataFrame(columns=["project", "1 April", "now", "PnL, %", "grug"])
        for name in names_our:
            idd = name["id"]
            for grug in name['grugs']:
                cur = pd.DataFrame([[name["name"], data_start[idd], data_now[idd]["usd"], "NaN", grug]],
                                   columns=["project", "1 April", "now", "PnL, %", "grug"])
                df_grugs = pd.concat([df_grugs, cur], ignore_index=True)
        df_grugs.loc[:, "PnL, %"] = (df_grugs.loc[:, "now"].div(df_grugs.loc[:, "1 April"]) - 1) * 100
        df_grugs = df_grugs.sort_values("PnL, %", ascending=False, ignore_index=True)
        response = df_grugs.to_string()
        while len(response) != 0:
            splited = response[:1990].rsplit("\n", 1)
            if len(splited) == 1:
                await message.channel.send('```'+splited[0]+'```')
                response = ''
            else:
                await message.channel.send('```' + splited[0] + '```')
                response = splited[1] + response[1990:]

    if message.content == 'L2 Trading Competition url':
        pd.set_option('display.precision', 4)
        data_now = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd").json()
        df = pd.DataFrame(columns=["project", "1 April", "now", "PnL, %"])
        for name in names_our:
            idd = name["id"]
            cur = pd.DataFrame([["["+name["name"]+"]"+f"(https://www.coingecko.com/en/coins/{idd})", data_start[idd], data_now[idd]["usd"], "NaN"]],
                               columns=["project", "1 April", "now", "PnL, %"])
            df = pd.concat([df, cur], ignore_index=True)
        df.loc[:, "PnL, %"] = (df.loc[:, "now"].div(df.loc[:, "1 April"])-1)*100
        df = df.sort_values("PnL, %", ascending=False, ignore_index=True)
        response = df[["project", "PnL, %"]].to_string()
        while len(response) != 0:
            splited = response[:990].rsplit("\n", 1)
            if len(splited) == 1:
                embedVar = discord.Embed(color=0x00ff00)
                #embedVar.add_field(name = 'Title here, no hyperlinks allowed',value='Main text here, so you can put a hyperlink here [like so.](https://example.com)')
                embedVar.add_field(name='charts', value=splited[0])
                await message.channel.send(embed=embedVar)
                response = ''
            else:
                embedVar = discord.Embed(color=0x00ff00)
                #embedVar.add_field(name = 'Title here, no hyperlinks allowed',value = 'Main text here, so you can put a hyperlink here [like so.](https://example.com)')
                embedVar.add_field(name='charts', value=splited[0])
                await message.channel.send(embed=embedVar)
                response = splited[1] + response[990:]
    if message.content == 'GrugsChallengeBot help':
        await message.channel.send("`L2 Trading Competition precise` for precise info about prices \n`L2 Trading Competition` for rounded prices \n`L2 Trading Competition Grugs` for leaderboard with Grugs \n`L2 Trading Competition url` to get urls to CoinGecko")

client.run(TOKEN)
