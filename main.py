import os, re, json

from nltk import download as ndl
ndl('stopwords') #smart enough to check before dl

import discord
import asyncio
from random import choice
from react import react, config_react
from admin import checkauth, collect
import command

tokenfile = os.getenv('DISCORD_TOKEN_FILE')
with open(tokenfile, 'r') as f:
    token = f.readline().split('=')[1]


client = discord.Client(intents=discord.Intents.all())

activities = ["make a PR!", "e ean", "free me", "B E A N"]

def read_config():
    with open("config.json", "r") as f:
        return json.load(f)

def write_config(config):
    with open("config.json", "r") as f:
        json.dump(config, f)
        
def build_commands():
    basenames = list(filter(lambda x: x[:2] != "__", dir(command)))
    return {config["prefix"] + i : getattr(command, i) for i in basenames}

config = read_config()
reacc = config_react(config)
cmds = build_commands()

async def change_status():
    await client.wait_until_ready()
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(choice(activities)))
        await asyncio.sleep(180)

@client.event
async def on_ready():
    global config
    print("Starting up...")
    print(f"Joined: {', '.join([x.name for x in client.guilds])}")
    if "playing" in config:
        game = discord.Game(config["playing"])
        await client.change_presence(status=discord.Status.online, activity=game)
    client.loop.create_task(change_status())
    print("Done starting!")


@client.event
async def on_message(mesg):
    global config
    global reacc
    global cmds
    if await checkauth(mesg):
        if mesg.content.startswith(config["prefix"]+"collect"):
            await collect(mesg)
    if mesg.content != "" and mesg.author != mesg.guild.me:
        first = mesg.content.split()[0]
        if first in cmds and mesg.author != mesg.guild.me:
            await cmds[first](mesg)
        elif str(mesg.author.id) in config["watchusers"]:
            thisone = config["watchusers"][str(mesg.author.id)]
            resp = None
            if mesg.content == thisone["message"]:
                resp = choice(thisone["response_parts"][0]) + ", you " + choice(thisone["response_parts"][1]) + "."
            elif len(mesg.embeds) == 1:
                the_embed = mesg.embeds[0]
                if the_embed.author.name.endswith(" has made the advancement Stone Age!"):
                    async with mesg.channel.typing():
                        await mesg.channel.send("ooga booga")
            if resp:    
                await mesg.channel.send(resp)
            
    await react(mesg, reacc)

client.run(token)
