import spacy, nltk, os, discord

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

    async for m in message.channel.history(limit=None):
        if m.author == t_mem:
            await message.channel.send(f"{m.author.name} be like:\n {m.content}")
            break

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
        names = [i for i in globals() if i[0] != "_"]
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


