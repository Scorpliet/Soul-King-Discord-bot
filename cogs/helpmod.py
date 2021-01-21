import discord
from discord.ext import commands
from embedss import help_em
import math
command_name={"join":"Joins a voice channel", 
"summon":"", 
"play":"Plays a song based on search query (url is not supported yet)", 
"pause":"Pauses the current playing song", 
"resume":"Resumes a currently paused song", 
"now":"Shows the currently playing song", 
"shuffle":"Shuffles the queue", 
"remove":"Removes a song from the queue with specified index", 
"skip":"Skips the current song based on 2 votes though the song requester can skip it without votes", 
"queue":"Displays the queue with songs to be played", 
"stop":"Stops playing song and clears the queue (doesn't leave the voice channel)", 
"leave":"Clears the queue and leaves the voice channel", 
"loop":"Repeats the current song, invoke the command again to unloop", 
"wordguess":"think of a word and the bot will guess it based on your input", 
"do":"requires an helping verb arg (do, does, will, should, are, is, has, have + you/I + anything) \n```example: brook should I go to sleep``` \n```brook does @EpicUser cry when he sleeps```" ,
"see my pants":"brook sends a an embeded image with reaction",
"45": "brook sends a random 45 degree embed, an inside joke"}

cmd_aliase={ 
"summon":"", 
"play":"p", 
"pause":"pau", 
"resume":"res", 
"now":"'current', 'playing'", 
"shuffle":"sh", 
"remove":"rem", 
"skip":"'next','n'", 
"queue":"q", 
"stop":"stop", 
"leave":"'disconnect', 'dis'", 
"loop":"'l', 'repeeat'", 
"wordguess":"'word', 'guess'", 
}






class Help(commands.Cog):
    def __init__(self, bot):
       self.bot = bot

    @commands.command(name="help", aliases=["hp"])
    async def help(self, ctx, commandname=None):
      """Shows this message"""
      if commandname is None:
         em=help_em.helpem
         await ctx.send(embed=em)
      else:
          newem= discord.Embed(name="help command", title=commandname+" info", description="**Description** \n"+command_name[commandname], color= discord.Color.gold())
          if commandname in cmd_aliase:
              newem.set_footer(text="aliases: "+cmd_aliase[commandname])
          await ctx.send(embed=newem)
    
    @commands.command(name="ping")
    async def ping(self,  ctx):
         pingem=discord.Embed(name="Ping", title="Pong :ping_pong:")
         pingem.add_field(name="WS Latency", value=f'`{round(self.bot.latency *1000, 2)}ms`', inline=True)
         msg = await ctx.send("\u200d")
         await msg.delete() 
         ms = (msg.created_at-ctx.message.created_at).total_seconds() * 1000      
         pingem.add_field(name="Response Time", value=f"`{ms}ms`", inline=True)
         await ctx.send(embed=pingem)

#@commands.command(name="about")
       


     

    


















def setup(bot):
   bot.add_cog(Help(bot))

