import discord
from jikanpy import AioJikan
from emoji import UNICODE_EMOJI
import aiohttp
async def lastMessage(ctx, users_id: int):
    oldestMessage = None
    fetchMessage = await ctx.channel.history().find(lambda m: m.author.id == users_id)

    if oldestMessage is None:
        oldestMessage = fetchMessage
    else:
        if fetchMessage.created_at > oldestMessage.created_at:
            oldestMessage = fetchMessage

    if (oldestMessage is not None):
        return oldestMessage.content 

  
def bot_owner(ctx):
    return ctx.message.author.id == 395230256828645376     

import asyncio

async def edit_msg_after(msg, content, delay):
     await asyncio.sleep(delay)
     await msg.edit(content=content)

async def mangasearch(self, ctx, *,query):
    """Search anime/manga from MyAnimeList.net"""
    aio_jikan = AioJikan()
    
    if query == '':
      await ctx.send('`You need to enter a manga name`')
      return


    if query in UNICODE_EMOJI:
      await ctx.send('`Emjois are not allowed`')
      return 

    async with ctx.channel.typing():

      results = await aio_jikan.search('manga', query)
      #results= await aio_jikan.search('anime', message)
      info = results.get('results')
      ids = []

      if info == ids:
        await ctx.send('`No results found`')
        return

  
      for x in range(5):
        ids.append(info[x].get('mal_id'))
  
      desc =  ''

      for x in range(5):
        url = 'https://api.jikan.moe/v3/manga/' + str(ids[x])
        async with aiohttp.ClientSession() as session:
          data = await self.fetch(session, url)

        if x == 4:
          if data.get('title_english') == None:
            desc += '**·** **' + data.get('title') + '**'

          elif data.get('title_english').lower() != data.get('title').lower():
            desc += '**·** **' + data.get('title') + '**\n' + '--' + data.get('title_english')

          elif data.get('title_english').lower() == data.get('title').lower():
            desc += '**·** **' + data.get('title') + '**'

        else:
          if data.get('title_english') == None:
            desc += '**·** **' + data.get('title') + '**\n'

          elif data.get('title_english').lower() != data.get('title').lower():
            desc += '**·** **' + data.get('title') + '**\n' + '--' + data.get('title_english') + '\n'

          elif data.get('title_english').lower() == data.get('title').lower():
            desc += '**·** **' + data.get('title') + '**\n'

  
      embed = discord.Embed(
        title = '**RESULTS**',
        description = desc,
        colour = discord.Color.gold(),
      )

      embed.set_footer(text = 'brook manga <title> to get more information')

      await aio_jikan.close()

      await ctx.send(embed = embed)