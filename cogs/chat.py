import discord
from discord.ext import commands
import random
from random import randrange
from funcs import lastMessage
from main import presponses, pemojies





seperator=' '

class chat(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  
  @commands.command(name="do", aliases=["should", "will", "are", "have", "would"])
  async def do(ctx, arg1, *args):
    """do a 45, do you anything, do I anything """
    pchance=randrange(8)
    message = await lastMessage(ctx, ctx.message.author.id)
    word = message.split()[1]
    
    if arg1=="you" or arg1=="u":
        if word=="are":
            word="am"  
        response = [f"Oh yes! I {word} ", f"Yohohoho! I {word} ", f"I {word} "]
        randomres = random.choice(response)
        if randomres == response[2]:
              await ctx.send(randomres + "{}".format(seperator.join(args)) + " Yohohoho!")
              if pchance==4:
               await ctx.send(random.choice(presponses)+random.choice(pemojies)) 
        else:
            await ctx.send(randomres + "{}".format(seperator.join(args)))
            if pchance==4:
               await ctx.send(random.choice(presponses)+
               random.choice(pemojies)) 
    elif arg1=="i":      
         response2 = ["How should I know that ", f"Maybe you {word} ", "You should ", "You must ", f"Yes, you {word} ", "Ofcourse ", "Clearly ", "You used to ", "No ", "Dont ", "You better not "]
         await ctx.send(random.choice(response2) + ctx.message.author.name + "-san")
         if pchance==4:
           await ctx.send(random.choice(presponses) + random.choice(pemojies))
    elif arg1=="a" and args[0]=="45":
        Images = [
        "https://i.pinimg.com/originals/ed/d5/36/edd536243dab449c0cd7c9d483d36b89.jpg",
        "https://pbs.twimg.com/media/EXnqC26XQAYFUbO.jpg",
        "https://i.ytimg.com/vi/uGJpB_PF_2s/maxresdefault.jpg",
        "https://i.ytimg.com/vi/Ho14w9MRjw0/maxresdefault.jpg",
        "https://media1.tenor.com/images/22b95af3a67e2af80fd098e2512dce73/tenor.gif?itemid=15220851"
         ]
        embed = discord.Embed(title="45 Degrees!")
        #embed.set_author(
        #name="Brook",
        #icon_url=
        #"https://i.pinimg.com/originals/cc/7e/e9/cc7ee92ea65e30f45482f8f2199ec69b.jpg")
        embed.set_image(url=random.choice(Images))
        await ctx.send(embed=embed)