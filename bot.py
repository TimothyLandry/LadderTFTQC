import discord
from discord.ext import tasks
import json
import time
import asyncio

from leaderboard import *

config = json.load(open("./config.json"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logo = open("./logo.txt").read()
    logo = logo.replace("VERSION_REPLACE", config["version"])
    logo = logo.replace("TIMESTAMP_PLACE", time.strftime("%Y-%m-%d %H:%M:%S"))

    channel = client.get_channel(config["channelId"])
    await channel.send(logo)
    cronLeaderboard.start()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Connected on {client.user}")

@tasks.loop(hours=3)
async def cronLeaderboard():
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - cronLeaderboard start")
    channel = client.get_channel(config["channelId"])

    profiles = await asyncio.to_thread(getProfiles)
    await channel.send(f"```fix\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {getRankLeaderboard(profiles)}```")
    await channel.send(f"```fix\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {getThreeStarsLeaderboard(profiles)}```")
    await channel.send(f"```fix\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {getCurrentSetAugmentsLeaderboard(profiles)}```")
    #await channel.send(f"```fix\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {getRecombobulatorLeaderboard(profiles)}```")
    
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} update sent.")

client.run(config["discordToken"])