import discord
from discord.ext import tasks
import json
import time
import asyncio

from leaderboard import getLeaderboardOutput

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
    cron_leaderboard.start()

@tasks.loop(hours=1)
async def cron_leaderboard():
    print('Starting cron_leaderboard')
    channel = client.get_channel(config["channelId"])

    output = await asyncio.to_thread(getLeaderboardOutput)
    await channel.send(output)

client.run(config["discordToken"])