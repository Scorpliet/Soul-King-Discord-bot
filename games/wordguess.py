import discord
import random
import asyncio

async def tpose(array): #Transpose function i copied from internet
        return [ [row[c] for row in array if c < len(row)] for c in range(0, max([len(row) for row in array])) ]

async def join_list(list):
        result=''
        for elements in list:
          result +=str(elements)  
        return result

alphabet=[
        ['A','B','C','D'], ['E','F','G','H'], ['I','J','K','L'], ['M','N','O','P'], ['Q','R','S','T'], ['U','V','W','X'], ['Y','Z','_','_']
        ] 


async def play(self, ctx): 
    while True:
      col_options=[]
      alpha_tpose=[]
      alpha_tpose2=[]
      final_word=[]
      endgame=False    

      responses=[", Yohoho! I guessed your word",
      ", oh you challenged me, Traveller?",
      ", am I the Akinator now? :sunglasses:",
      ", I guessed your word {}-san".format(ctx.author.name),
      ", sometimes my intellect is ascended",
      ]              



      em=discord.Embed(title="``` 1  2  3  4```")
      em.set_author(
        name=ctx.author.name+"-san\'s game")
      em.set_thumbnail(url=ctx.author.avatar_url)
      em.set_footer(text="Timeout: 30s | Type \"end\" to end the game")  

      
      em2=discord.Embed(title="``` 1  2  3  4  5  6  7```")
      em2.set_author(
        name=ctx.author.name+"-san\'s game")
      em2.set_thumbnail(url=ctx.author.avatar_url)
      em2.set_footer(text="Timeout: 30s | Type \"end\" to end the game")
      
      endembed = discord.Embed(title="Game ended", description="by "+ctx.author.name)
      endembed.set_thumbnail(url=ctx.author.avatar_url)
     
      
      

      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
                          
      try:
         while True:
           ques = await ctx.send("What is the length of your word")
           msg = await self.bot.wait_for('message', check=check, timeout=20)
           try:
              if msg.content=="end":
                 await ctx.send("Game ended")
                 await msg.add_reaction('👍')
                 endgame=True
                 break
              else:  
                 length = int(msg.content)
                 break
           except Exception: 
               await ctx.send("That is not a number \nType end to quit")
               await ques.delete()  
      except asyncio.TimeoutError:
         await ctx.send("Game ended. You didn\'t respond in time")  
         endgame=True
      
      if endgame==True:
         break
           

      for i in range(6):             
          em.add_field(name=alphabet[i], value='\u200b', inline=False)
      em.add_field(name=['Y','Z'], value='\u200b', inline=False)
              
        
      
      embed1 = await ctx.send(embed=em)
      
    
      x = 1
      while x <=length:
            try:       
                 msg = await ctx.send("Whats the column of letter {}".format(x))
                 guessinput = await self.bot.wait_for('message',  check=check, timeout=30)
                 if guessinput.content=="end":
                    await embed1.edit(embed=endembed)      
                    await guessinput.add_reaction("👍")
                    await msg.delete()                
                    break
                 guessinp = int(guessinput.content)               
                 if guessinp >4 or guessinp<1:
                       await ctx.send("That column doesn't exists baka")
                       await msg.delete()
                 else:    
                       col_options.append(guessinp) #adding the input value in a  list so it can be fetched later
                       x = x+1
                       await msg.delete()
            except asyncio.TimeoutError:
                 await ctx.send("Oops! There was no response")

                 break
      
      if col_options==[]:
        break
              


      for i in col_options:
              alp2=tpose(alphabet) #Transposed the array
              alpha_tpose.append(alp2[i-1]) #added selected columns in new array
    
      length_max_value = len(max(alpha_tpose, key=len))
      range_of_array = len(alpha_tpose)
      
      
      for i in range(range_of_array):
            async with ctx.typing(): 
               em2.add_field(name=alpha_tpose[i], value='\u200b', inline=False)

      embed2 = await ctx.send(embed=em2)    
      col_options.clear()
      x=1    
    
      while x<=length: 
              try:                  
                 msg = await ctx.send("Whats the column of letter {}".format(x))
                 guessinput = await self.bot.wait_for('message', check=check, timeout=30) 
                 if guessinput.content=="end":
                    await embed2.edit(embed=endembed)      
                    await guessinput.add_reaction("👍")
                    await msg.delete()               
                    break              
                 guessinp = int(guessinput.content)
                 if guessinp>length_max_value or guessinp<1:
                     await ctx.send("That column doesn't exists baka:")
                 else:
                     col_options.append(guessinp) #adding the input value in a list so it can be fetched later
                     x = x+1
                     await msg.delete()
              except asyncio.TimeoutError:
                 await ctx.send("Oops! There was no response")
                 await embed2.delete()
                 break      
      if col_options==[]:
        break
    
      for i in col_options:
              alp3=tpose(alpha_tpose)
              alpha_tpose2.append(alp3[i-1])
      
      col_options.clear()
      length_max_value2 = len(max(alpha_tpose2, key=len))
   
      #for i in range(length_max_value2):
             #await ctx.send(alpha_tpose2[i])  
   
      for i in range(length_max_value2):
               j=i 
               final_word.append((alpha_tpose2[i][j]))  
      async with ctx.typing():
       await ctx.send("Your word was " + join_list(final_word)+ random.choice(responses))
       break