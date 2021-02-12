from discord.ext import commands
from cogs.funcs import bot_owner
import discord
import os
import sys
token = os.environ.get("TOKEN")
class admintools(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.check(bot_owner)
  async def reload(self,ctx, mod=None):
    modules = ["game","helpmod","music","chat","image","mal"]
    self.bot.reload_extension("jishaku")   
    if mod==None:
      try:
        for module in modules:
            self.bot.reload_extension('cogs.'+module)
      except Exception as e:
        await ctx.author.send(f"Unable to load {module}: \n{e}")      
      await ctx.send(":repeat: Reloaded all extensions")
    else:
      try:
        self.bot.reload_extension('cogs.'+mod)
        await ctx.send(":repeat: Reloaded "+mod)
      except Exception as e:
        await ctx.message.add_reaction("exclamation")
        await ctx.author.send(f"Unable to load {mod}: \n{e}")    
  
  @commands.command(name="ping")
  async def ping(self, ctx):
         pingem=discord.Embed(name="Ping", title="Pong :ping_pong:")
         pingem.add_field(name="WS Latency", value=f'`{round(self.bot.latency *1000, 2)}ms`', inline=True)
         msg = await ctx.send("\u200d")
         await msg.delete() 
         ms = (msg.created_at-ctx.message.created_at).total_seconds() * 1000      
         pingem.add_field(name="Response Time", value=f"`{ms}ms`", inline=True)
         await ctx.send(embed=pingem)
  
  @commands.command()
  @commands.check(bot_owner)
  async def restart(self,ctx):
    await ctx.send("Restarting...")
    #await ctx.send("Wait")
    #await ctx.bot.logout()
    #await ctx.bot.login(token, bot=True)
    python = sys.executable
    os.execl(python, python, * sys.argv)

def setup(bot):
  bot.add_cog(admintools(bot))        