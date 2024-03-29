import nltk, os, discord, types
import numpy as np
from collections import Counter

DISCORD_MESSAGE_SIZE = 2000

async def belike(message):
    """Gets the last message user sent in this channel.

    Usage: belike <user>"""
    try:
        t_name = message.content.split(" ")[1].lower()
    except IndexError:
        await message.channel.send("**Error:** You must specify a name or nickname!")
    for pm in message.channel.members:
        if (pm.nick or pm.name).lower() == t_name:
            t_mem = pm
            break
    else:
        await message.channel.send(f"**Error:** could not find user by name or nick `{t_name}`");
        return

    async for m in message.channel.history(limit=200):
        if m.author == t_mem and m.id != message.id:
            await message.channel.send(f"{m.author.nick or m.author.name} be like:\n {m.content}")
            return
    await message.channel.send(f"**Error:** {t_mem.nick or t_mem.name} hasn't said anything recently enough!")

async def help(message):
    """Shows help, either for all commands or help and usage for a specific command.

    Usage: help [command]"""
    arg = message.content.split(" ")
    if len(arg) > 1:
        try:
            await message.channel.send("```" + arg[1] + ": " + globals()[arg[1]].__doc__ + "```")
        except KeyError:
            await message.channel.send(f"**Error:** `{arg[1]}` does not match any command.")
    else:
        names = [i for i in globals() if i[0] != "_" and isinstance(globals()[i], types.FunctionType)]
        withdoc = [i + ": " + globals()[i].__doc__.split("\n")[0] for i in sorted(names)]
        await message.channel.send("```" + "\n".join(withdoc) + "```")

sr = nltk.corpus.stopwords.words('english')
async def wordfreq(message):
    """Find the most frequent significant word in the past n messages

    Usage: wordfreq [n]
    - n defaults to 200 and has a max of 10,000"""
    global sr
    arg = message.content.split(" ")
    if len(arg) < 2:
        n = 1000
    else:
        n = min(10000, int(arg[1]))
    async with message.channel.typing():
        tokens = []
        ctr = 0
        async for m in message.channel.history(limit=n):
            ctr += 1
            tokens.extend([i.strip() for i in m.clean_content.split(" ") if i.strip() != ""])

        cleantokens = tokens[:]
        for t in tokens:
            if t in sr:
                cleantokens.remove(t)
        freq = nltk.FreqDist(cleantokens)
        top10 = freq.most_common(10)
        names = [i[0] for i in top10]
        ns = len(max(names, key=len))
        datastr = "\n".join(map(lambda x: f"{x[0]:>{ns}}: {x[1]:<}", top10))
        await message.channel.send(f"```Frequencies [read {ctr}/{n} messages]:\n{'word':>{ns}}: {'count':<}\n" + datastr + "```")

async def talkative(message):
    """Find the n most talkative people in the last m messages in this channel

    Usage: talkative [n] [m]
    - n defaults to 5
    - m defaults to 500 and has a max of 10,000"""
    arg = message.content.split(" ")
    if len(arg) > 1:
        n = int(arg[1])
    else:
        n = 5
    if len(arg) > 2:
        mct = min(10000, int(arg[2]))
    else:
        mct = 500
    async with message.channel.typing():
        senders = {}
        ctr = 0
        async for m in message.channel.history(limit=mct):
            ctr += 1
            if m.author.id == None:
                continue
            if (m.author.id in senders):
                senders[m.author.id] += 1
            else:
                senders[m.author.id] = 1
        msend = sorted([(i, senders[i]) for i in senders], key=(lambda x: x[1]), reverse=True)
        tot = list(map(lambda x: (message.guild.get_member(x[0]), x[1]), msend[:n]))
        tot = list(map(lambda y: ((y[0].nick or y[0].name if not y[0] == None else "Unknown User"), y[1]), tot))
        rmax = max(len(str(n)) + 1, len("Rank"))
        nmax = max(len(max(tot, key=(lambda x: len(x[0])))[0]), len("Name"))
        cmax = len(str(max(tot, key=(lambda x: len(str(x[1]))))[1]))
        hdr = f"{'Rank':>{rmax}}: {'Name':>{nmax}}: {'Messages'}\n"
        elems = [f"{'#'+str(i+1):>{rmax}}: {tot[i][0]:>{nmax}}: {tot[i][1]:>{cmax}}" for i in range(len(tot))]
        fmt = f"```Top talkers [read {ctr}/{mct} messages]:\n" + hdr + "\n".join(elems) + "```"
        await message.channel.send(fmt)

async def mostmsg(msg):
    """Find the most typical message in the last n messages, by looking at the most frequent character in each position.
    Setting strict to `y` means 'no character' counts as a candidate for most frequent, making the message much shorter.

    Usage: mostmessage [strict] [n]

    - n defaults to 2000
    - strict defaults to `n`
    """
    arg = msg.content.split(" ")
    n = 2000
    strict = False
    if len(arg) > 1:
        strict = (arg[1].lower() == 'y')
        if len(arg) > 2:
            n = int(arg[2])
    async with msg.channel.typing():
        total = 0
        letters = []
        async for m in msg.channel.history(limit=n):
            for i in range(len(m.content)):
                try:
                    letters[i] += m.content[i]
                except IndexError:
                    assert i == len(letters), f"Tried to skip over character at position {i}!"
                    letters.append(m.content[i])
            total += 1
        res = ""
        for pos in letters:
            cts = Counter(pos)
            winner = max(cts, key=lambda x: cts[x])
            if strict and cts[winner] < (total - len(pos)):
                break
            res += winner
        await msg.channel.send(f"{res}\n`Polled {total}/{n} messages`")