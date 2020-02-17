import os

import discord

token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#to get a specific reaction, simply type \:reaction: in your server
beano = "<:beano:678811304034566144>"
@client.event
async def on_message(mesg):
    await mesg.add_reaction(beano)

client.run(token)
