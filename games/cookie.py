import discord
import random
import time
import asyncio

async def add_reactions(list, msg, t1):
   for i in list:
      t1 = time.perf_counter() 
      await msg.add_reaction(i)  
   return t1

async def play(self, ctx):
  
  food = ["🍪","🍣", "🌯", "🥞","🌮","🍩","🌭"]
  reactions = []
  seclected_food = random.choice(food)
  reactions.append(seclected_food)
  #sh_food = random.sample(food, len(food))
  random.shuffle(food)
  for i in range(0,random.randint(4,5)):
     reactions.append(food[i])

  #sh_reaction = random.sample(reactions, len(reactions))
  random.shuffle(reactions)

  embed = discord.Embed(name="cookie", title=f"Eat the {seclected_food}")
  embed.add_field(name="In 5 seconds", value="\u200d", inline =False)
  #embed.set_thumbnail(url="games/res/brook3.png")
  embed.color=discord.Color.gold()
  em = await ctx.send(embed=embed) 
  
  def check(reaction, user):
        return reaction.message.guild == ctx.guild and reaction.message.channel == ctx.message.channel and reaction.message == em and str(reaction.emoji) == seclected_food and user != ctx.bot.user and not user.bot
  
  for i in reversed(range(1,5)):
      await asyncio.sleep(1)
      embed.set_field_at(0, name=f"In {i} seconds", value ="\u200d", inline =False)
      await em.edit(embed=embed)
  
  await asyncio.sleep(1)  
  embed.set_field_at(0, name="Now", value ="\u200d", inline =False)
  await em.edit(embed=embed)
  await asyncio.sleep(random.randint(0,1))
  if reactions[0] == seclected_food:
    try: 
      await em.add_reaction(reactions[0])
      t1 = time.perf_counter()   
      reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
      t2=time.perf_counter()
    except asyncio.TimeoutError:
            await ctx.send("No one ate it")  
    
    
  else:
    try:
      for i in reactions:
        await asyncio.sleep(0.01)
        t1 = time.perf_counter() 
        await em.add_reaction(i) 
      #await add_reactions(reactions, em, t1)        
      reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
      t2 = time.perf_counter() 
    except asyncio.TimeoutError:
            await ctx.send("No one ate it")
    
  em2= discord.Embed()
  em2.set_thumbnail(url=user.avatar_url)
  em2.add_field(name='Winner', value =f"**{user}** ate it in **{round(t2-t1,3)}s**", inline =False)
  em2.set_footer(icon_url= ctx.author.avatar_url , text=f"Game requested by {ctx.author}")
  em2.color=discord.Color.gold()
  await em.edit(embed=em2)       
     
  


  
 
  