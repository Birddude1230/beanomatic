import os, re

import discord

token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#to get a specific reaction, simply type \:reaction: in your server
beano = "<:beano:670475306515169280>"

react_cond = re.compile(".*[b🅱️ ]ean.*")
bean_role = None
@client.event
async def on_message(mesg):
    global bean_role
    text = mesg.content
    roles = mesg.author.roles
    if bean_role == None:
        for i in mesg.guild.roles:
            if i.name == "beaned":
                bean_role = i
    if (react_cond.match(text) or (bean_role in roles)):
        await mesg.add_reaction(beano)

client.run(token)
