import discord
from discord.ext import commands
from games import wordguess, userpoints, cookie, battle
from cogs.funcs import bot_owner
from PIL import Image, ImageDraw, ImageFont
import aiohttp
from io import BytesIO
import random
bounty_list=["30,000,000 \U000023af","120,000,000 \U000023af","15,000,000 \U000023af","45,000,000 \U000023af","50","47,000,000 \U000023af","80,000,000 \U000023af","79,000,000","300,000,000","400,000,000","50","100","10,000,000","100,000,000","40,000,000","320,000,000","500,000,000","77,000,000","100"]
class games(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  
  @commands.command(name="wordguess", aliases=["guess", "word"], description=
  "Think of a word, Ill guess it")
  async def word_guess(self,ctx):
    await wordguess.play(self,ctx)


  @commands.command(name="points", aliases=["profile"]) 
  async def point(self,ctx):
    await userpoints.balpoints(ctx)
    
  
  @commands.command(name="addvalor0987")
  @commands.check(bot_owner)
  async def valor(self, ctx, user:discord.Member=None):
    if user==None:
       await userpoints.addvalor(ctx.author, change=1, mode="valor") 
    else:
       await userpoints.addvalor(user, change=1, mode="valor")
  
  @commands.command(name="leaderboard", aliases=["lb"])
  async def leaderboard(self, ctx):
    await userpoints.leaderboard(self, ctx,x = 10)

  @commands.command(name="top", aliases=["serverboard"])
  async def top(self, ctx):
    await userpoints.top(self, ctx,x = 10)  
  
  @commands.max_concurrency(1, per=commands.BucketType.channel)
  @commands.command(name="cookie", aliases=["cupcake", "c", "sushi", "taco", "burrito", "eat", "khao"]) 
  async def _cookie(self,ctx):
    """Eat the given dish before anyone else!"""
    await cookie.play(self, ctx)

  @commands.max_concurrency(2, per=commands.BucketType.channel)
  @commands.command(name="fight", aliases=["battle", "duel", "lrwao", "phudda", "phuda","phada"]) 
  async def _fight(self,ctx, user: discord.Member=None):
    """Duel with members in intense battle"""  
    await battle.fight(self, ctx, user)
  



def setup(bot):
   bot.add_cog(games(bot))     