import discord
from discord.ext import commands
import asyncio
import random
import json
from fuzzywuzzy import fuzz
from io import BytesIO
from PIL import Image
import aiohttp
class body:
  def __init__(self, member, health):
    self.member=member
    self.health=health

async def versus_embed(ctx, member_user, user_user, phrase):
  async with aiohttp.ClientSession() as cs:
        async with cs.get(str(member_user.avatar_url)) as r:
            avt_bytes = ""await r.read()
        async with cs.get(str(user_user.avatar_url)) as r:
            user_avt_bytes = await r.read()    
  avatar1 = Image.open(BytesIO(avt_bytes))
  avatar2 = Image.open(BytesIO(user_avt_bytes)) 
  poster  = Image.open("games/res/versus.png")
  avatar1 = avatar1.resize((600,600))
  avatar2 = avatar2.resize((600,600))
  poster.paste(avatar1, (100,200))
  poster.paste(avatar2, (1400,200))
  #poster  = poster.resize((700,400))
  output  = BytesIO()
  poster.save(output, "png")
  output.seek(0)
  vsimage = discord.File(fp=output, filename="vs.png")
  #await ctx.send(file=vsimage)
  embed=discord.Embed(description=random.choice(phrase))
  embed.set_image(url="attachment://vs.png")
  await ctx.send(file=vsimage, embed=embed)


  


sentences=["gomu gomu no pistol", "gomu gomu no rifle", "Onigiri"]
async def damage_mutliplier(stringa, stringb):
       score = fuzz.ratio(stringa, stringb)
       #if "":
       damage = score*0.25
       return await damage
       #print(len(''.join(stringa)))
       #a,b = stringa.casefold(), stringb.casefold()
       #for a,b in zip(a,b): 
          #print(a, b)


#damage_mutliplier("gomu gomu no pistol", "gomi gomi ni pist")
    

async def fight(self, ctx, user: discord.Member=None):
   if user is None:
      await ctx.send("Well, who do you want to fight")
      return
   else:
      try:
         user=ctx.message.mentions[0]
      except IndexError:
         return await ctx.send("Mention the person you want to duel")
            
      selected_sentence=''
      async def send_sentences():
         return await ctx.send(random.choice(sentences))
      async def damage_mutliplier(selected_sentence):
         result=[]
         for elements in selected_sentence:
           result.append()

      #member_author=ctx.author   
      
      challenge=[
      f"{ctx.author.mention} picked a fight with {user.mention}",
      f"{ctx.author.mention} challenged {user.mention} to a duel"]
      
      def check(msg):
        return msg.author==ctx.author and msg.channel==ctx.channel
      health = 100

      def check2(msg):
        return msg.author==user and msg.channel==ctx.channel
      
      member=body(ctx.author, health) 
      user1=body(user, health)

      #await ctx.send("your health {}".format(member.health))
      #await ctx.send(user.health)

      fighting=True
      
      await ctx.send(random.choice(challenge))
      while fighting and member.health>0 and user1.health>0:
        #msg = await ctx.send(f"What do you want to do {ctx.author.mention}\n`fight` `end`")
        await versus_embed(ctx, ctx.author, user, challenge)
        #await self.bot.wait_for("message", check=check, timeout=30)
        
        break

     