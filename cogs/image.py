import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
from io import BytesIO
import random
bounty_list=[" 30,000,000"," 120,000,000"," 15,000,000"," 45,000,000"," 50"," 47,000,000"," 80,000,000"," 79,000,000"," 300,000,000"," 400,000,000"," 50","  100"," 10,000,000"," 100,000,000"," 40,000,000"," 320,000,000"," 500,000,000"," 77,000,000"," 100"]
class images(commands.Cog):
  def __init__(self, bot):
       self.bot = bot
 
 
  @commands.command()
  async def wanted(self, ctx,user: discord.User=None):
    """Generate your wanted poster with your bounty"""
    if user is None:
          user = ctx.author
    async with aiohttp.ClientSession() as cs:
        async with cs.get(str(user.avatar_url)) as r:
            avt_bytes = await r.read()
    avatar = Image.open(BytesIO(avt_bytes))
    avatar = avatar.resize((607,424))
    poster = Image.open("res/WantedPoster.jpg")
    poster.paste(avatar, (60,222))
    
    fnt1 = ImageFont.truetype("res/simsun.ttc", 75)
    text1=user.name.upper()
    img_fraction = 0.80
    fontsize=1
    fnt = ImageFont.truetype("res/mingliub.ttc", fontsize) 
    #128
    while fnt.getsize(text1)[0] < img_fraction*poster.size[0]:
          fontsize += 1
          fnt = ImageFont.truetype("res/mingliub.ttc", fontsize)

    fontsize -= 1
    if fontsize >=128:
      fontsize=128
    
    fnt = ImageFont.truetype("res/mingliub.ttc", fontsize)
    ImageDraw.Draw(poster).text((72,720), font=fnt, fill="#382727",text=user.name.upper(), stroke_width=2)
    ImageDraw.Draw(poster).text((135,850), font=fnt1, fill="#382727",text=random.choice(bounty_list), stroke_width=1)
    output = BytesIO()
    poster.save(output, "png")
    output.seek(0)
    await ctx.send(file = discord.File(fp=output, filename="wanted.png"))
  


def setup(bot):
   bot.add_cog(images(bot))         