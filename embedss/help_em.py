import discord
text = "here"
target = "https://github.com/Scorpliet/SoulKing/blob/main/README.md"
link=(f"[{text}]({target})")


thumbnails=["https://i.gifer.com/4BQA.gif", "https://i.pinimg.com/originals/55/e0/b8/55e0b8141326fefeec11e7fb9bdaaa09.gif","https://i.imgur.com/BMn77BO.gif","https://i.imgur.com/5IzN3YF.gif"]
helpem=discord.Embed(name="Help", title="Help", description="Prefix: brook help or .help \nType brook help command for more info on a command" +"\n", color= discord.Color.gold())
helpem.set_author(name="Brook", icon_url=thumbnails[1]) 
helpem.set_thumbnail(url=thumbnails[0])
helpem.add_field(name=":wave: Greetings", value="`hello brook` `hello soulking`",
      inline=False)
helpem.add_field(name=":speech_balloon: Chat", value="`45` `see my pants`\n`To chat: \nrequires an helping verb arg (do, have, will, should, are, + you/I/we + anything)`\n`(does, is, has + anything)`", inline=False)
helpem.add_field(name=":musical_note: Music", value="`join` `summon` `play` `pause`, `resume` `now` `shuffle` `remove` `skip` `queue` `stop` `leave` `loop`", inline=False)
helpem.add_field(name=":game_die: Games", value="`wordguess` `cookie`", inline=False)
helpem.add_field(name=":new: Upcoming Features", value = "`**Games**: duel (b/w 2 members) and more games` \n `points and rank system on winning games` \n`**New Image Category**`", inline=False)
helpem.set_footer(text="\n Creator: @scorpliet#5803")



