import discord
from discord.ext import commands
import asyncio
import random
import json


class body:
  def __init__(self, member, health):
    self.member=member
    self.health=health

sentences=["gomu gomu no pistol", "gomu gomu no rifle", "Onigiri"]
def damage_mutliplier(stringa, stringb):
       damage=0
       print(len(''.join(stringa)))
       a,b = stringa.casefold(), stringb.casefold()
       for a,b in zip(a,b): 
          print(a, b)


damage_mutliplier("gomu gomu no pistol", "gomi gomi ni pist")
    

async def fight(self, ctx, user: discord.Member):
   if user is None:
      await ctx.send("Well who do you want to fight")
      return
   else:      
      selected_sentence=''
      async def send_sentences():
         return await ctx.send(random.choice(sentences))
      async def damage_mutliplier(selected_sentence):
         result=[]
         for elements in selected_sentence:
           result.append()
         

      try:
         user=ctx.message.mentions[0]
      except IndexError:
         return await ctx.send("Mention the person you want to duel")
      
      challenge=[
      f"{ctx.author.mention} picked a fight with {user}",
      f"{ctx.author.mention} challenged {user} to a duel"]
      
      def check(msg):
        return msg.author==ctx.author and msg.channel==ctx.channel
      health = 100
      
      member=body(ctx.author, health) 
      user=body(user, health)

      #await ctx.send("your health {}".format(member.health))
      #await ctx.send(user.health)

      fighting=True
      
      await ctx.send(random.choice(challenge))
      while fighting and member.health>0 and user.health>0:
        msg = await ctx.send(f"What do you want to do {ctx.author.mention}")
        break

     