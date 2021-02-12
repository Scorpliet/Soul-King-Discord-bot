import json
import discord
import typing
ranks = ["Recruit", "Initiate", "Novice", "Apprentice","Adept"]
amount = [0,50,100,200,300,400]
  
#async def savepoints():
   #with open("data.json", "w") as f:
     #return users=json.dump(users, f)
     

async def getpoints():
  with open("data.json", "r") as f:
        users=json.load(f)
  return users   




async def newpoints(user):
  users = await getpoints()
  if str(user.id) in users:
    return False 
  else:
    users[str(user.id)] ={}
    users[str(user.id)]["berries"] = 0 
    users[str(user.id)]["bounty"] = 0
    users[str(user.id)]["rank"] = "Recruit"
  with open("data.json", "w") as f:
    users=json.dump(users, f)



async def balpoints(ctx):
  await newpoints(ctx.author)  
  user = ctx.author     
  users = await getpoints()
  point_amt = users[str(user.id)]["berries"]
  valor_amt = users[str(user.id)]["bounty"]
  valor_rank = users[str(user.id)]["rank"]
  embed = discord.Embed(title=f"{user.name}'s profile")
  embed.set_thumbnail(url=user.avatar_url)
  embed.add_field(name="```Berries```", value=point_amt)
  embed.add_field(name="```Bounty```", value=valor_amt, inline=True)
  embed.add_field(name="```Rank```", value=valor_rank, inline=True)
  await ctx.send(embed=embed)

async def addpoints(user, change=0, mode="berries"):
    users = await getpoints()
    users[str(user.id)][mode] += change
    with open("data.json", "w") as f:
       users=json.dump(users, f)
    return user

async def addvalor(user, change=0, mode="bounty"):
    users = await getpoints()
    users[str(user.id)][mode] += change 
    bounty = users[str(user.id)][mode]
    leng = len(amount)   
    for i in range(leng):
      if bounty == 0:
        rank="Recruit"
      elif bounty>amount[i-1] and bounty<=amount[i]:
          if bounty<50:
            rank = ranks[i-1]
          else:
            rank=ranks[i]    
      else: 
        continue 
    users[str(user.id)]["rank"] = rank
    with open("data.json", "w") as f:
       users=json.dump(users, f)
    return user

async def top(self, ctx, mode1: typing.Optional[str]="berries", mode2: typing.Optional[str]="bounty", x = 10):
    users = await getpoints()
    leader_board = {}
    total = []
    guild = ctx.guild
    for user in users:
        name = int(user)
        points_amount = users[user]["berries"]
        valor_amount =  users[user]["bounty"]
        rank = users[user]["rank"]
        leader_board[points_amount, valor_amount] = name
        #total.append(total_amount)

    total = sorted(leader_board ,key=lambda l:l[1]
    ,reverse=True)    
    
    em = discord.Embed(
    title = "Global Leaderboard", 
    # description = "`          berries   bounty   Rank`",
    color = discord.Color.gold())
    index = 1
    top_list = []
    for p,v in total:
        id_ = leader_board[p,v]
        member = self.bot.get_user(id_)
        name = member.name
        if index==1 or index==2 or index==3:
            top_list.append(f"**{name}** » {p} {v}, {rank}")
        else:
            top_list.append(f"**{name}** » {p} {v}, {rank}")    
        if index == x:
            break
        else:
            index += 1
    top_list_final = "\n".join(top_list[0:x])        
    em.add_field(name="\u200d", value=f'{top_list_final}')
    await ctx.send(embed = em)

async def leaderboard(self, ctx, mode1: typing.Optional[str]="berries", mode2: typing.Optional[str]="bounty", x = 10):
    users = await getpoints()
    leader_board = {}
    total = []
    guild = ctx.guild
    for user in users:
        name = int(user)
        points_amount = users[user]["berries"]
        valor_amount =  users[user]["bounty"]
        rank = users[user]["rank"]
        leader_board[points_amount, valor_amount] = name
        #total.append(total_amount)
  
    total = sorted(leader_board ,key=lambda l:l[1]
    ,reverse=True)    
    
    em = discord.Embed(
    title = f"{guild.name} Leaderboard", 
    # description = "`          berries   bounty   Rank`",
    color = discord.Color.gold())
    index = 1
    top_list = []

    for p,v in total:
        id_ = leader_board[p,v]
        member = self.bot.get_user(id_)
        name = member.name
        if member in guild.members:
          if index==1 or index==2 or index==3:
             top_list.append(f"**{name}** » {p} {v}, {rank}")
          else:
             top_list.append(f"**{name}** » {p} {v}, {rank}")    
          if index == x:
            break
          else:
            index += 1
    top_list_final = "\n".join(top_list[0:x])        
    em.add_field(name="\u200d", value=f'{top_list_final}')
    await ctx.send(embed = em)
