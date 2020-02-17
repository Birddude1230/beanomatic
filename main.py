import os, re

import discord

token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#to get a specific reaction, simply type \:reaction: in your server
beano = "<:beano:670475306515169280>"


react_cond = re.compile(r".*[b🅱️ B]\s*[eE]\s*[aA]\s*[nN].*")
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
    game = discord.Game("with beano")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("Done starting!")

@client.event
async def on_message(mesg):
    global bean_role
    text = mesg.content
    roles = mesg.author.roles
    if (react_cond.match(text) or (bean_role in roles) or mesg.channel.name == "beano"):
        await mesg.add_reaction(beano)

client.run(token)
