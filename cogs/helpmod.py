import discord
from discord.ext import commands
import random
from fuzzywuzzy import process
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
"45": "brook sends a random 45 degree embed, an inside joke",
"cookie": "Get the cookie and rate and beat your time"}

command_list=["join", 
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
"do",
"see my pants",
"45",
"cookie"]

    
    
thumbnails=["https://i.gifer.com/4BQA.gif", "https://i.pinimg.com/originals/55/e0/b8/55e0b8141326fefeec11e7fb9bdaaa09.gif","https://i.imgur.com/BMn77BO.gif","https://i.imgur.com/5IzN3YF.gif"]
#@commands.command(name="about")
       
class CustomHelpCommand(commands.HelpCommand):
    """
    Custom help command.
    """
    
    
    async def send_bot_help(self, _):
         helpem=discord.Embed(name="Help", title="Help", description="Prefix: brook help or .help \nType brook help command for more info on a command" +"\n", color= discord.Color.gold())
         helpem.set_author(name="Brook", icon_url=thumbnails[1]) 
         helpem.set_thumbnail(url=random.choice(thumbnails))
         helpem.add_field(name=":wave: Greetings", value="`hello brook` `hello soulking`",
                       inline=False)
         helpem.add_field(name=":speech_balloon: Chat", value="`45`  `see my pants`\n`To chat: Refer advanced help with brook help do/does`",inline=False)
         helpem.add_field(name=":frame_photo: Images", value="`wanted`", inline=False)
         helpem.add_field(name=":game_die: Games", value="`wordguess` `cookie`", inline=False)
         helpem.add_field(name=":magic_wand: Info/Utility", value="`ping` `anime` `manga` `user` `schedule`", inline=False)
         helpem.add_field(name=":musical_note: Music", value="`join` `summon` `play` `pause`, `resume` `now` `shuffle` `remove` `skip` `queue` `stop` `leave` `loop`", inline=False)
         helpem.add_field(name=":new: Upcoming Features", value = "`**Games**: duel (b/w 2 members) and more    games` \n `points and rank system on winning games` \n`**New Image Category**`", inline=False)
         helpem.set_footer(text="\n Creator: @scorpliet#5803")

         
         await self.context.send(embed=helpem)

    async def send_command_help(self, command):  
        embed = discord.Embed(title=f"{command.name} info",
                              description=f'*{command.help}*',
                              colour=discord.Color.gold())
        #embed.add_field(name="Signature:", value=f"{command.name} {command.signature}", inline=False)
        embed.add_field(name="\u200d", value=f"**Category:** {command.cog_name}")
        #embed.add_field(name="\u200d", value=f"**Category:** {command.cog_name}", inline=False)
        if command.name == "do" or command.name== "does":
          pass          
        else:  
         embed.add_field(name="Aliases:", value=", ".join(command.aliases) or "None", inline=False)
        embed.set_thumbnail(url=self.context.bot.user.avatar_url)
        embed.set_footer(
            text="Type brook help (command) for more info on a command.\n"
            "You can also type brook help (category) for more info on a category.")
        return await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"Help on Category `{cog.qualified_name}`",
                              description=cog.description or None,
                              colour=discord.Color.gold())
        embed.add_field(name="Commands in this Category:", value="`"+"` `".join(str(command) for command in cog.get_commands())+"`" or "None")
        embed.set_thumbnail(url=self.context.bot.user.avatar_url)
        embed.set_footer(
            text="Type brook help (command) for more info on a command.\n"
            "You can also type brook help (category) for more info on a category.")
        return await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"Help on Command Group `{group.name}`",
                              description=group.help or "No info available.",
                              colour=discord.Color.gold())
        embed.add_field(name="Signature:", value=f"{group.name} {group.signature}", inline=False)
        embed.add_field(name="Category:", value=f"{group.cog_name}", inline=False)
        try:
            can_run = await group.can_run(self.context)
            if can_run:
                can_run = self.context.bot.emoji_dict["green_tick"]
            else:
                can_run = self.context.bot.emoji_dict["red_tick"]
        except commands.CommandError:
            can_run = self.context.bot.emoji_dict["red_tick"]
        embed.add_field(name="Can Use:", value=can_run)
        embed.add_field(name="Aliases:", value="\n".join(group.aliases) or "None", inline=False)
        embed.add_field(name="Commands in this Group:", value="\n".join(str(command) for command in group.walk_commands()) or "None")
        embed.set_thumbnail(url=self.context.bot.user.avatar_url)
        embed.set_footer(
            text="Type brook help (command) for more info on a command.\n"
            "You can also type brook help (category) for more info on a category.")
        return await self.context.send(embed=embed)

    async def command_not_found(self, string):
        match, ratio = process.extractOne(string, command_list)
        if ratio < 50:
            return f"Command '{string}' is not found."
        return f"Command '{string}' is not found. Did you mean `{match}`?"


def setup(bot):
    bot.help_command = CustomHelpCommand()


def teardown(bot):
    bot.help_command = None

#def setup(bot):
   #bot.add_cog(Helpmod(bot))

