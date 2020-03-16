import os, pickle, discord

async def checkauth(message):
    if (message.author.permissions_in(message.channel) >= discord.Permissions(0x00000010)):
        return True
    return False

"""async def prefix(message, config):
    args = message.split(" ")
    if len(args) > 2:
        await message.channel.send("**Error:** No prefix supplied!")
    else:
        config["prefix"] = args[1]
        await message.channel.send(f"Set prefix to `{args[1]}`")"""

async def collect(message):
    fn = f"{message.channel.id}.dat"
    if os.path.isfile(fn):
        await message.channel.send("**Error:** already collected this channel!")
        return
    await message.channel.send("Collecting channel...")
    print(f"COLLECTING CHANNEL {message.channel.name} {message.channel.id}")
    cdat = []
    with open(fn, "wb") as f:
        async for m in message.channel.history(limit=None):
            if m.clean_content != "":
                cdat.append((m.clean_content, m.author.id))
            if ((len(cdat)) % 10000) == 0:
                await message.channel.send(f"Read {len(cdat)} nonempty messages so far...")
        pickle.dump(cdat, f)
    await message.channel.send(f"Channel collected! Saved {len(cdat)} messages to file.") 
