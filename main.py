import os, re

import discord

token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#to get a specific reaction, simply type \:reaction: in your server
beano = "<:beano:670475306515169280>"

react_cond = re.compile(".*[b🅱️ ]ean.*")
@client.event
async def on_message(mesg):
    text = mesg.content
    print(text)
    if (react_cond.match(text)):
        await mesg.add_reaction(beano)

client.run(token)
