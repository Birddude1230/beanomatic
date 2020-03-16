import os, re, json

import discord
from react import react, config_react
from admin import checkauth, collect
import command

token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

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

@client.event
async def on_ready():
    global config
    print("Starting up...")
    print(f"Joined: {', '.join([x.name for x in client.guilds])}")
    if "playing" in config:
        game = discord.Game(config["playing"])
        await client.change_presence(status=discord.Status.online, activity=game)
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
            
    await react(mesg, reacc)

client.run(token)
