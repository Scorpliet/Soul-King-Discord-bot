import discord

text = "here"
target = "https://github.com/Scorpliet/SoulKing/blob/main/README.md"
link=(f"[{text}]({target})")

helpem=discord.Embed(name="Help", title="Help", description="Prefix: brook help or .help \nTo get detailed help refer "+ link)
helpem.set_author(name="Brook") 
helpem.set_thumbnail(url="https://i.gifer.com/4BQA.gif")
helpem.add_field(name="Greetings", value="```hello brook, hello soulking```",
      inline=False)
helpem.add_field(name="Commands", value="```45, ,see my pants\ndo: requires an helping verb arg (do, will, should, are + you/I + anything)\ndoes: (does, has, is + user+ anything)```", inline=False)
helpem.add_field(name=":musical_note: Music", value="```join, summon, play, pause, resume, now, shuffle, remove, skip, queue stop, leave, loop, volume```", inline=False)
helpem.add_field(name=":game_die: Games", value="```wordguess```", inline=False)
helpem.set_footer(text="Type brook help command for more info on a command \n| Creator: @scorpliet#5803")