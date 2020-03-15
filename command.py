import nltk, os, discord, types

async def belike(message):
    """Gets the last message user sent in this channel.

    Usage: belike <user>"""
    t_name = message.content.split(" ")[1] 
    for pm in message.channel.members:
        if pm.nick == t_name or pm.name == t_name:
            t_mem = pm
            break
    else:
        await message.channel.send(f"**Error:** could not find user by name or nick `{t_name}`");
        return

    async for m in message.channel.history(limit=200):
        if m.author == t_mem and m.id != message.id:
            await message.channel.send(f"{m.author.nick or m.author.name} be like:\n {m.content}")
            return
    await message.channel.send(f"**Error:** {m.author.nick or m.author.name} hasn't said anything recently enough!")

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

async def tparse(message):
    """Generate parse tree for sentence. Not useful...

    Usage: tparse <sentence>"""
    arg = message.content.split(" ")
    if len(arg) < 2:
        await message.channel.send("**Error:** must provide input to parse")
        return
    if len(arg) > 50:
        await message.channel.send("**Error:** input too large!")
        return

    async with message.channel.typing():
        sent = " ".join(arg[1:])
        tokens = nltk.word_tokenize(sent)
        tagged = nltk.pos_tag(tokens)
        tree = nltk.chunk.ne_chunk(tagged)
        cf = nltk.draw.util.CanvasFrame()
        tc = nltk.draw.TreeWidget(cf.canvas(), tree)
        tc["node_font"] = 'arial 14 bold'
        tc["leaf_font"] = 'arial 14'
        tc['node_color'] = "#404b69"
        tc['leaf_color'] = "#00818a"
        tc['line_color'] = "#dbedf3"
        cf.add_widget(tc, 10, 10)
        cf.print_to_file("output.ps")
        cf.destroy()
        #nltk.draw.tree.TreeView(tree)._cframe.print_to_file("output.ps")
        os.system("convert -density 600 output.ps -resize 200% output.png")
        await message.channel.send(file=discord.File("output.png"))

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
        async for m in message.channel.history(limit=n):
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
        await message.channel.send(f"```Frequencies:\n{'word':>{ns}}: {'count':<}\n" + datastr + "```")

async def talkative(message):
    """Find the n most talkative people in the last m messages in this channel

    Usage talkative [n] [m]
    - n defaults to 5
    - m defaults to 500 and has a max of 10,000"""
    arg = message.content.split(" ")
    if len(arg) > 1:
        n = int(arg[1])
    else:
        n = 5
    if len(arg) > 2:
        m = max(10000, int(arg[2]))
    else:
        m = 500
    async with message.channel.typing():
        senders = {}
        async for m in message.channel.history(limit=m):
            if (m.author.id in senders):
                senders[m.author.id] += 1
            else:
                senders[m.author.id] = 1
        msend = sorted([(i, senders[i]) for i in senders], key=(lambda x: x[1]), reverse=True)
        tot = list(map(lambda x: (message.guild.get_member(x[0]), x[1]), msend[:n]))
        tot = list(map(lambda y: ((y[0].nick or y[0].name), y[1]), tot))
        rmax = max(len(str(n)) + 1, len("Rank"))
        nmax = max(len(max(tot, key=(lambda x: len(x[0])))[0]), len("Name"))
        cmax = len(str(max(tot, key=(lambda x: len(str(x[1]))))[1]))
        hdr = f"{'Rank':>{rmax}}: {'Name':>{nmax}}: {'Messages'}\n"
        elems = [f"{'#'+str(i+1):>{rmax}}: {tot[i][0]:>{nmax}}: {tot[i][1]:>{cmax}}" for i in range(len(tot))]
        fmt = "```Top talkers:\n" + hdr + "\n".join(elems) + "```"
        await message.channel.send(fmt)
