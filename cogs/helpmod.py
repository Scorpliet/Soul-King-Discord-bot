import discord
from discord.ext import commands
from embedss import help_em

command_name={"join", 
"summon", 
"play", 
"pause", 
"resume", 
"now", 
"shuffle", 
"remove", 
"skip", 
"queue", 
"stop", 
"leave", 
"loop", 
"volume",
"wordguess", 
"do",
"see"}

class Help(commands.Cog):
    def __init__(self, bot):
       self.bot = bot

    @commands.command()
    async def help(self, ctx, commandname=None):
      """Shows this message"""
      em=help_em.helpem
      await ctx.send(embed=em)
    #  if commandname:
       # newem= discord.Embed(name="help command", title=command_name)
       # await em.edit(embed=newem)
    
          
      

      

    


















def setup(bot):
   bot.add_cog(Help(bot))

