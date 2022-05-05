import discord
from discord.ext import commands
import random
from random import randrange
from cogs.funcs import lastMessage
#from main import presponses, pemojies

presponses = [
    #"Can you show me your panties ",
    ""
    #"uh, can I see your panties ",
    #"Would you mind showing me your panties ",
]
pemojies = [
    ":point_right::point_left:", ":flushed:", ":smirk:",
    ":face_with_hand_over_mouth:", ":weary:", ":grinning:", ":pleading_face:",
    ":eyes:", ":eye::eye:"
]

seperator = ' '


class chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="do",
                      aliases=["should", "will", "are", "have", "would"])
    async def do(self, ctx, arg1, *args):
        """requires an helping verb arg (do, does, will, should, are, is, has, have + you/I + anything) \n`example: brook should I go to sleep`\n`brook does @EpicUser cry when he sleeps`"""
        pchance = randrange(8)
        message = await lastMessage(ctx, ctx.author.id)
        word = message.split()[1]
        if arg1 == "you" or arg1 == "u":
            if word == "are":
                word = "am"
            elif word == "will":
                word = "would"
            response = [
                f"Oh yes! I {word} ", f"Yohohoho! I {word} ", f"I {word} ",
                f"No I {word}n't "
            ]
            randomres = random.choice(response)
            if randomres == response[2]:
                await ctx.send(randomres + "{}".format(seperator.join(args)) +
                               " Yohohoho!")
                if pchance == 4:
                    await ctx.send(
                        random.choice(presponses) + random.choice(pemojies))
            else:
                await ctx.send(randomres + "{}".format(seperator.join(args)))
                if pchance == 4:
                    await ctx.send(
                        random.choice(presponses) + random.choice(pemojies))
        elif arg1 == "i" or arg1 == "we":
            response2 = [
                "How should I know that ", f"Maybe you {word} ", "You should ",
                "You must ", f"Yes, you {word} ", "Ofcourse ", "Clearly ",
                "You used to ", "No ", "Dont ", "You better not "
            ]
            await ctx.send(random.choice(response2) + ctx.author.name + "-san")
            if pchance == 4:
                await ctx.send(
                    random.choice(presponses) + random.choice(pemojies))
        elif arg1 == "a" and args[0] == "45":
            Images = [
                "https://i.pinimg.com/originals/ed/d5/36/edd536243dab449c0cd7c9d483d36b89.jpg",
                "https://pbs.twimg.com/media/EXnqC26XQAYFUbO.jpg",
                "https://i.ytimg.com/vi/uGJpB_PF_2s/maxresdefault.jpg",
                "https://media1.tenor.com/images/22b95af3a67e2af80fd098e2512dce73/tenor.gif?itemid=15220851",
                "https://thumbs.gfycat.com/IdolizedFlimsyBluetonguelizard-small.gif"
            ]
            embed = discord.Embed(title="45 Degrees!")
            #embed.set_author(
            #name="Brook",
            #icon_url=
            #"https://i.pinimg.com/originals/cc/7e/e9/cc7ee92ea65e30f45482f8f2199ec69b.jpg")
            embed.set_image(url=random.choice(Images))
            await ctx.send(embed=embed)
        elif arg1 == discord.Member:
            resp = [f"{arg1} {word} "]
            await ctx.send(
                random.choice(resp) + "{}".format(seperator.join(args)))
        else:
            resp = [
                "No I cannot do that", "I wont",
                f"I'll die {word}ing that, wait I'm already dead Yohohoho!",
                "No",
                f"{word} you want me to die? Oh wait I'm already dead Yohohoho!"
            ]
            await ctx.send(random.choice(resp))

    @commands.command(name="does", aliases=["is", "has"])
    async def does(self, ctx, user,*args):
        """requires an helping verb arg (do, does, will, should, are, is, has, have + you/I + anything) \n`example: brook should I go to sleep`\n`brook does @EpicUser cry when he sleeps`"""
           
        message = await lastMessage(ctx, ctx.author.id)
        #message = message.replace("’","")
        #print(message)
        word = message.split()[1]
        response = [
            f"{user} {word} ", f"{user} definitely {word} ",
            f"{user} {word}n't ", f"How should I know if {user} {word} ",
            f"Yes I can confirm, {user} "
        ]
        await ctx.send(
            random.choice(response) + "{}".format(seperator.join(args)))

def setup(bot):
    bot.add_cog(chatbot(bot))
