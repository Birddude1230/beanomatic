import os, re

import discord

token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#to get a specific reaction, simply type \:reaction: in your server
beano = "<:beano:670475306515169280>"

react_cond = re.compile(".*[b🅱️ ]ean.*")
bean_role = None

@client.event
async def on_ready():
    global bean_role
    print("Starting up...")
    for g in client.guilds:
        for i in g.roles:
            if i.name == "beaned":
                bean_role = i
                print(f"Got beaned role on server {g.name}")
    print("Done starting!")

@client.event
async def on_message(mesg):
    global bean_role
    text = mesg.content
    roles = mesg.author.roles
    if (react_cond.match(text) or (bean_role in roles)):
        await mesg.add_reaction(beano)

client.run(token)
