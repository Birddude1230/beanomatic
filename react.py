import re

class Reaction():
    def __init__(self, name, reaction, pattern=None, role=None, channel=None):
        self.name = name
        self.reaction = reaction
        self.pattern = pattern
        self.role = role
        self.channel = channel

    async def handle_message(self, message):
        if self.pattern:
            if self.pattern.match(message.content):
                await message.add_reaction(self.reaction)
                return True
        if self.role:
            if self.role in message.author.roles:
                await message.add_reaction(self.reaction)
                return True
        if self.channel:
            if self.channel == message.channel.name:
                await message.add_reaction(self.reaction)
                return True

async def react(message, lis):
    for i in lis:
        await i.handle_message(message)

def config_react(config):
    res = []
    try:
        if "reactions" in config:
            for i in config["reactions"]:
                if "pattern" in i:
                    i["pattern"] = re.compile(i["pattern"])
                else:
                    i["pattern"] = None
                if not "role" in i:
                    i["role"] = None
                if not "channel" in i:
                    i["channel"] = None
                res.append(Reaction(**i))
    except KeyError:
        print("Could not find expected key in reaction! Is there a reaction missing a name or emote?")
    return res
