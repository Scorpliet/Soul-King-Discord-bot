import json
import discord

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
    users[str(user.id)]["points"] = 0 
    users[str(user.id)]["valor"] = 0
    users[str(user.id)]["rank"] = "Recruit"
  with open("data.json", "w") as f:
    users=json.dump(users, f)



async def balpoints(ctx):
  await newpoints(ctx.author)  
  user = ctx.author     
  users = await getpoints()
  point_amt = users[str(user.id)]["points"]
  valor_amt = users[str(user.id)]["valor"]
  valor_rank = users[str(user.id)]["rank"]
  embed = discord.Embed(title=f"{user.name}'s profile")
  embed.set_thumbnail(url=user.avatar_url)
  embed.add_field(name="```Points```", value=point_amt)
  embed.add_field(name="```Valor```", value=valor_amt, inline=True)
  embed.add_field(name="```Rank```", value=valor_rank, inline=True)
  await ctx.send(embed=embed)

async def addpoints(user, change=0, mode="points"):
    users = await getpoints()
    users[str(user.id)][mode] += change
    with open("data.json", "w") as f:
       users=json.dump(users, f)
    return user

async def addvalor(user, change=0, mode="valor"):
    users = await getpoints()
    users[str(user.id)][mode] += change 
    valor = users[str(user.id)][mode]
    leng = len(amount)   
    for i in range(leng):
      if valor == 0:
        rank="Recruit"
      elif valor>amount[i-1] and valor<=amount[i]:
          if valor<50:
            rank = ranks[i-1]
          else:
            rank=ranks[i]    
      else: 
        continue 
    users[str(user.id)]["rank"] = rank
    with open("data.json", "w") as f:
       users=json.dump(users, f)
    return user

async def leaderboard(self, ctx,x = 10):
    users = await getpoints()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        points_amount = users[user]["points"]
        valor_amount =  users[user]["valor"]
        rank = users[user]["rank"]
        leader_board[points_amount, valor_amount] = name
        #total.append(total_amount)

    total = sorted(leader_board, key=lambda l:l[1], reverse=True)    
    
    em = discord.Embed(title = "Brook's Leaderboard" , description = "Globally",color = discord.Color(0xfa43ee))
    index = 1
    for p,v in total:
        id_ = leader_board[p, v]
        member = self.bot.get_user(id_)
        name = member.name
        em.add_field(name = f":blue_circle: {name}" , value = f"{rank}",  inline = True)
        em.add_field(name = "Points", value = f'{p}', inline= True)
        em.add_field(name="Valor", value= f'{v},({rank})', inline=True)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)