#Importing all modules

import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
from keep_alive import keep_alive
from random import randrange
from embedss import help_em
token = os.environ.get("TOKEN")
# TO DOWNLOAD FFMPEG:
# ctrl+shift+s
# npm install ffmpeg-static
# node -e "console.log(require('ffmpeg-static'))"
# copy result to variable below:
intents=discord.Intents.all()


FFMPEG_PATH = '/home/runner/dsbottsk2/node_modules/ffmpeg-static/ffmpeg'
discord.opus.load_opus("./libopus.so.0.8.0")
bot = commands.Bot(
  command_prefix=('brook ', "."), 
  case_insensitive=True,
  intents=intents,
  description="A Strawhat who has joined your guild")
bot.remove_command('help')


presponses=["Can you show me your panties ",
"uh, can I see your panties ",
"Would you mind showing me your panties ",

]
pemojies=[":point_right::point_left:",
":flushed:",
":smirk:",
":face_with_hand_over_mouth:",
":weary:",
":grinning:",
":pleading_face:",
":eyes:", ":eye::eye:"
]



#Adding bg task
status = cycle(['Binks Sake', 'Binks Sake'])


@bot.event
async def on_ready():
    change_status.start()
    print("{0}".format(bot.user))

    #bot.kclient = ksoftapi.Client(os.environ['KToken'])
    #bot.client = ClientSession()
    modules = ["game","helpmod","music"]
    try:
        for module in modules:
            bot.load_extension('cogs.'+module)
            print('Loaded: ' + module)
    except Exception as e:
        print(f'Error loading {module}: {e}')

    print('Im ready')

text = "here"
target = "https://github.com/Scorpliet/SoulKing/blob/main/README.md"


@bot.event
async def on_guild_join(guild):
    helpem= help_em.helpem
    system_channel= guild.system_channel  
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await system_channel.send(embed=helpem)
            #await channel.send('Hey there! Thank you for adding me!\nMy prefix is `~`\nStart by typing `~help`')
            break

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    await bot.process_commands(message)  #This line makes sure on_message wont take priority over a command function
    pchance=randrange(8)
    if message.content.startswith(("hello brook", "hello soulking", "hi brook", "hey brook")):
        randomliststart = [
            "Yohohoohoohoo! Hello, ", "Konnichiwa, ",
            "https://pa1.narvii.com/6280/3b9059c399eadd18056b566e13e34a364fda337e_hq.gif",
            "Moshi Moshi :snail: "
        ]

        randomlistend = ["-san"]
        response = random.choice(randomliststart)
        if response == randomliststart[2]:
            await message.channel.send(response)
            if pchance==4:
               await message.channel.send(random.choice(presponses)+random.choice(pemojies))
        else:
            await message.channel.send(response + message.author.name +random.choice(randomlistend))
            if pchance==4:
               await message.channel.send(random.choice(presponses)+random.choice(pemojies))
    elif message.content.startswith(("brook see my pants",".see my pants", "brook see my panties")):
        Images = [
        "https://24.media.tumblr.com/d7b5d85b4e1ed9e9e8022e9f728eff63/tumblr_mtaaqhnXxa1rf3uloo1_400.gif",
        "https://pa1.narvii.com/6331/7e3067290368f17896cf42b4a300870feb4a8fc8_00.gif" ]
        embed = discord.Embed()
        #embed.set_author(
        #name="Brook",
        #icon_url=
        #"https://i.pinimg.com/originals/cc/7e/e9/cc7ee92ea65e30f45482f8f2199ec69b.jpg")
        embed.set_image(url=random.choice(Images))
        await message.channel.send(embed=embed)


@bot.command(name="see")
async def see(ctx):
    """see your pants o_O"""
    pass
@bot.command(name="45")
async def brook45(ctx):
    """45 Degrees!"""
    pchance=randrange(8)
    Images = [
        "https://i.pinimg.com/originals/ed/d5/36/edd536243dab449c0cd7c9d483d36b89.jpg",
        "https://pbs.twimg.com/media/EXnqC26XQAYFUbO.jpg",
        "https://i.ytimg.com/vi/uGJpB_PF_2s/maxresdefault.jpg",
        "https://i.ytimg.com/vi/Ho14w9MRjw0/maxresdefault.jpg",
        "https://media1.tenor.com/images/22b95af3a67e2af80fd098e2512dce73/tenor.gif?itemid=15220851"]
    embed = discord.Embed(title="45 Degrees!")
        #embed.set_author(
        #name="Brook",
        #icon_url=
        #"https://i.pinimg.com/originals/cc/7e/e9/cc7ee92ea65e30f45482f8f2199ec69b.jpg")
    embed.set_image(url=random.choice(Images))
    await ctx.send(embed=embed)
    if pchance==4:
           await ctx.send(random.choice(presponses) + random.choice(pemojies))


async def lastMessage(ctx, users_id: int):
    oldestMessage = None
    fetchMessage = await ctx.channel.history().find(lambda m: m.author.id == users_id)

    if oldestMessage is None:
        oldestMessage = fetchMessage
    else:
        if fetchMessage.created_at > oldestMessage.created_at:
            oldestMessage = fetchMessage

    if (oldestMessage is not None):
        return oldestMessage.content

seperator=' '


@bot.command(aliases=["should", "will", "are", "have", "would"], description="Do anything YOHOHO!, (do a 45, do you poop, do I poop)")
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
  
          
@bot.command(name="does", aliases=["is", "has"])
async def trydoes(ctx, user: discord.Member, *args):
  message = await lastMessage(ctx, ctx.message.author.id)
  word = message.split()[1]
  try:
     response=[f"{user.name} {word} ", f"{user.name} definitely {word} ", f"{user.name} {word}n't ", f"How should I know if {user.name} {word} ", f"Yes I saw {user.name} "]
     await ctx.send(random.choice(response) + "{}".format(seperator.join(args)))
  except Exception:
     message = await lastMessage(ctx, ctx.message.author.id)
     word = message.split()[2]
     response=[f"{word} does ", f"{word} definitely does ", f"{word} doesn't ", f"How should I know if {word} does ", f"Yes I saw {word} "] 
     await ctx.send(random.choice(response) + "{}".format(seperator.join(args)))


keep_alive()
bot.run(token)
