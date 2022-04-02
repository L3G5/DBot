# bot.py
import os
import random
import requests
import pandas as pd
import numpy as np
import tabulate
from table2ascii import table2ascii, PresetStyle

import discord
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.environ['DISCORD_TOKEN']


client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'L2 Trading Competition Leaderboard':
        names_our = [{'id': 'nft-worlds', 'symbol': 'wrld', 'name': 'NFT Worlds'},
                     {'id': 'treasure-under-sea', 'symbol': 'tus', 'name': 'Treasure Under Sea'},
                     {'id': 'crabada', 'symbol': 'cra', 'name': 'Crabada'},
                     {'id': 'lords', 'symbol': 'lords', 'name': 'LORDS'},
                     {'id': 'magic', 'symbol': 'magic', 'name': 'Magic'},
                     {'id': 'rainbow-token-2', 'symbol': 'rbw', 'name': 'Rainbow Token'},
                     {'id': 'unicorn-milk', 'symbol': 'unim', 'name': 'Unicorn Milk'},
                     {'id': 'xpendium', 'symbol': 'xpnd', 'name': 'Xpendium'},
                     {'id': 'verse', 'symbol': 'verse', 'name': 'Verse'},
                     {'id': 'immutable-x', 'symbol': 'imx', 'name': 'Immutable X'},
                     {'id': 'illuvium', 'symbol': 'ilv', 'name': 'Illuvium'},
                     {'id': 'gods-unchained', 'symbol': 'gods', 'name': 'Gods Unchained'},
                     {'id': 'splinterlands', 'symbol': 'sps', 'name': 'Splinterlands'},
                     {'id': 'dark-energy-crystals',
                      'symbol': 'dec',
                      'name': 'Dark Energy Crystals'},
                     {'id': 'decentral-games-ice', 'symbol': 'ice', 'name': 'Decentral Games ICE'},
                     {'id': 'metis-token', 'symbol': 'metis', 'name': 'Metis Token'},
                     {'id': 'skale', 'symbol': 'skl', 'name': 'SKALE'},
                     {'id': 'crypto-raiders', 'symbol': 'raider', 'name': 'Crypto Raiders'},
                     {'id': 'layer2dao', 'symbol': 'l2dao', 'name': 'Layer2DAO'},
                     {'id': 'axie-infinity', 'symbol': 'axs', 'name': 'Axie Infinity'},
                     {'id': 'dydx', 'symbol': 'dydx', 'name': 'dYdX'},
                     {'id': 'loopring', 'symbol': 'lrc', 'name': 'Loopring'},
                     {'id': 'omisego', 'symbol': 'omg', 'name': 'OMG Network'},
                     {'id': 'zkspace', 'symbol': 'zks', 'name': 'ZKSpace'},
                     {'id': 'cartesi', 'symbol': 'ctsi', 'name': 'Cartesi'},
                     {'id': 'iotex', 'symbol': 'iotx', 'name': 'IoTeX'}]
        ids = []
        for name in names_our:
            ids.append(name["id"])
        ids_str = ",".join(ids)
        data_now = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd").json()
        data_start = {}
        for name in names_our:
            idd = name["id"]
            price_arr = requests.get(
                f"https://api.coingecko.com/api/v3/coins/{idd}/history?date=01-04-2022&localization=false").json()
            try:
                data_start[name["id"]] = price_arr["market_data"]["current_price"]["usd"]
            except KeyError:
                data_start[name["id"]] = np.nan
        df = pd.DataFrame(columns=["name", "1 April", "now", "PnL, %"])
        for name in names_our:
            idd = name["id"]
            cur = pd.DataFrame([[name["name"], data_start[idd], data_now[idd]["usd"], "NaN"]],
                               columns=["name", "1 April", "now", "PnL, %"])
            df = pd.concat([df, cur], ignore_index=True)
        df.loc[:, "PnL, %"] = (df.loc[:, "now"].div(df.loc[:, "1 April"])-1)*100
        df = df.sort_values("PnL, %", ascending=False, ignore_index=True)

        output = table2ascii(
            header=list(df.columns),
            body=df.values.tolist(),
        )

        response = '```'+df.to_string()+'```'
        await message.channel.send(response)

client.run(TOKEN)
