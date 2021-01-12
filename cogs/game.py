import discord
from discord.ext import commands
from games import wordguess, userpoints

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
  async def valor(self, ctx):
    await userpoints.addvalor(ctx.author, change=1, mode="valor") 

  
  @commands.command(name="leaderboard", aliases=["lb"])
  async def leaderboard(self, ctx):
    await userpoints.leaderboard(self, ctx,x = 1)





 
  


def setup(bot):
   bot.add_cog(games(bot))     