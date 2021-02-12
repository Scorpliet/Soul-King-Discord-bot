import discord
import json
import aiohttp
import requests
from emoji import UNICODE_EMOJI
from jikanpy import AioJikan
from discord.ext import commands
import typing

class MyAnimeList(commands.Cog):
  def __init__(self, bot):
    self.client = bot
    self.url = 'https://graphql.anilist.co'
     
  @commands.command(aliases=["ani"])
  async def anime(self, ctx, *, message):
    """Display anime details from MyAnimeList.net"""
    if message[:4] == 'mal ':
      message = message[4:]
      await self.malani(ctx, message)

    elif message[:3] == 'al ':
      message = message[3:]
      await self.alani(ctx, message)

    else:
      await self.alani(ctx, message)
  

  async def malani(self, ctx, message):
    aio_jikan = AioJikan()
    
    if message == '':
      await ctx.send('Well what show?')
      return

    else:
      message = message.lower()

    if message in UNICODE_EMOJI:
      await ctx.send('`Emjois are not allowed`')
      return

    async with ctx.channel.typing():

      results = await aio_jikan.search('anime', message)
      info = results.get('results')

      check = []
      if info == check:
        await ctx.send('`No results found`')
        return

      info = info[0]
      show = info.get('mal_id')
      title = info.get('title').lower()
 
      url = 'https://api.jikan.moe/v3/anime/' + str(show)
      async with aiohttp.ClientSession() as session:
        data = await self.fetch(session, url)
 
      img = data.get('image_url')
      title = data.get('title')
      num_ep = data.get('episodes')
      status = data.get('status')
      score = data.get('score')
      rank = data.get('rank')
      pop = data.get('popularity')
      genres = data.get('genres')
  

      genre = ''
      for x in genres:
        if x.get('name') == 'Hentai':
          await ctx.send('`That is not allowed in this channel`')
          return

        if x != genres[len(genres) - 1]:
          genre += x.get('name') + ', '

        else:
          genre += x.get('name')
  
  
  
      #handles dates of the show airing
      aired = data.get('aired')
      start = aired.get('from')
      end = aired.get('to')

      if start == None:
        start = 'Not Yet Aired'
        num_ep = 'None'
        end = 'Not Yet Aired'
  
      elif start != None:
        start = start[:10]
 
      if num_ep == None and start != None:
        num_ep = 'Currently Airing'


      if end == None and start != None:
        end = 'On Going'

      elif end != 'Not Yet Aired':
        end = end[:10]

      link = data.get('url')
      author = data.get('title_english')
      if author == title:
        author = None
  
      #handles the synopsis for show
      description = data.get('synopsis')
      description = description[:255]
      description += '...'


      embed = discord.Embed(
        title = '**' + title +'**',
        description = author,
        colour = discord.Color.gold(),
        url = link
      )


      embed.set_thumbnail(url = img)
      embed.add_field(name = 'Status', value = status)
      embed.add_field(name = 'Number of episodes', value = num_ep)
      embed.add_field(name = 'Score / Popularity / Rank', value = 'Score: ' + str(score) + ' / Popularity: ' + str(pop) + ' / Rank: ' + str(rank), inline = False)
      embed.add_field(name = 'Started Airing', value = start)
      embed.add_field(name = 'Finished Airing', value = end)
      embed.add_field(name = 'Synopsis', value = description, inline = False)
      embed.add_field(name = 'Genres', value = genre, inline = False)
      embed.set_footer(text = 'Replying to: ' + str(ctx.author) + ' | ' + 'info from MAL')

      await aio_jikan.close()

      await ctx.send(embed = embed)


  async def alani(self, ctx, message):
    async with ctx.channel.typing():

      query = '''
        query ($id: Int, $page: Int, $perPage: Int, $search: String, $type: MediaType) {
          Page (page: $page, perPage: $perPage) {
            pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
            }
            media (id: $id, search: $search, type: $type) {
              id
              description(asHtml: false)
              title {
                  english
                  romaji
              }
              coverImage {
                large
              }
              bannerImage
              averageScore
              meanScore
              status
              episodes
              genres
              popularity
              rankings{
                rank
                allTime
              }
              startDate{
                year
                month
                day
              }
              endDate{
                year
                month
                day
              }
              externalLinks{
                url
                site
              }
          }
      }
  }
'''

      variables = {
        'search': message,
        'page': 1,
        'type': 'ANIME'
      }

      response = requests.post(self.url, json={'query': query, 'variables': variables})
      #print(response.json())
      response = response.json()
      stuff = response.get('data')
      page = stuff.get('Page')
      page = page.get('media')
      media = page[0]
      img = media.get('coverImage')
      img = img.get('large')

      description = media.get('description')
      description = description.replace('<br>\n', ' ')
      description = description.replace('<br> ', ' ')
      description = description[:255]
      description += '...'


      titles = media.get('title')
      title = titles.get('romaji')
      title_eng = titles.get('english')

      score = float(media.get('averageScore')) / 10.0

      status = media.get('status')
      if status == 'FINISHED':
        status = 'Finished Airing'

      num_ep = media.get('episodes')

      popularity = media.get('popularity')
      rank = media.get('rankings')
      
      try:
        rank = rank[1]
     
      except IndexError:
        if len(rank) < 1:
          rank = 'N/A'

        else:
          rank = rank[0]

      if rank != 'N/A':
        rank = rank.get('rank')
      genres = media.get('genres')

      genre = ''
      for x in genres:
        if x == 'Hentai':
          await ctx.send('That is not allowed in this channel')
          return

        if x != genres[-1]:
          genre += x + ', '

        else:
          genre += x
      
      date = media.get('startDate')
      year = date.get('year')
      month = date.get('month')
      day = date.get('day')

      start = str(month) + '-' + str(day) + '-' + str(year)


      date = media.get('endDate')
      year = date.get('year')
      month = date.get('month')
      day = date.get('day')

      end = str(month) + '-' + str(day) + '-' + str(year)


      id = media.get('id')
      link = 'https://anilist.co/anime/' + str(id)




      embed = discord.Embed(
        title = '**' + title + '**',
        description = title_eng,
        colour = discord.Color.gold(),
        url = link
      )

      embed.set_thumbnail(url = img)
      embed.add_field(name = 'Status', value = status)
      embed.add_field(name = 'Number of episodes', value = num_ep)
      embed.add_field(name = 'Score / Popularity / Rank', value = 'Score: ' + str(score) + ' / Popularity: ' + str(popularity) + ' / Rank: ' + str(rank), inline = False)
      embed.add_field(name = 'Started Airing', value = start)
      embed.add_field(name = 'Finished Airing', value = end)
      embed.add_field(name = 'Synopsis', value = description, inline = False)
      embed.add_field(name = 'Genres', value = genre, inline = False)
      embed.set_footer(text = 'Replying to: ' + str(ctx.author) + ' | ' + 'info from Anilist')

      await ctx.send(embed = embed)
      return   
     
  @commands.command(aliases=["mang"])
  async def manga(self, ctx, search:typing.Optional[str]="search", *, message):
    """Display manga details from MyAnimeList.net\n
    Use `manga search` to search for manga"""  
    aio_jikan = AioJikan()
    
    if search =="search":
     async with ctx.channel.typing():

      results = await aio_jikan.search('manga', message)
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
      return
    
    
    if message == '':
      await ctx.send('`You need to enter a manga name`')
      return
    if message in UNICODE_EMOJI:
      await ctx.send('`Emjois are not allowed`')
      return  
    async with ctx.channel.typing():
      results = await aio_jikan.search('manga', message)
      info = results.get('results')

      check = []
      if info == check:
        await ctx.send('`No results found`')
        return

      info = info[0]
      show = info.get('mal_id')
      title = info.get('title').lower()
  
  
      url = 'https://api.jikan.moe/v3/manga/' + str(show)
      async with aiohttp.ClientSession() as session:
        data = await self.fetch(session, url)


      img = data.get('image_url')
      title = data.get('title')
  
      chapters = data.get('chapters')
      if chapters == None:
        chapters = 'Currently Publishing'

      status = data.get('status')
      score = data.get('score')
      rank = data.get('rank')
      pop = data.get('popularity')
      genres = data.get('genres')
  

      genre = ''
      for x in genres:
        if x.get('name') == 'Hentai':
          await ctx.send('`That is not allowed in this channel`')
          return

        if x != genres[len(genres) - 1]:
          genre += x.get('name') + ', '

        else:
          genre += x.get('name')
  
      #handles dates of the show airing
      aired = data.get('published')
      start = aired.get('from')
      end = aired.get('to')

      if start == None:
        start = 'Not Yet Published'
        end = 'Not Yet Published'
  
      elif start != None:
        start = start[:10]
 

      if end == None and start != None:
        end = 'On Going'

      elif end != 'Not Yet Published':
        end = end[:10]


      link = data.get('url')
      author = data.get('title_english')
      if author == title:
        author = None
  
      #handles the synopsis for show
      description = data.get('synopsis')
      description = description[:252]
      description += '...'


      embed = discord.Embed(
        title = '**' + title +'**',
        description = author,
        colour = discord.Color.gold(),
        url = link
      )


      embed.set_thumbnail(url = img)
      embed.add_field(name = 'Status', value = status)
      embed.add_field(name = 'Number of Chapters', value = str(chapters))
      embed.add_field(name = 'Score / Popularity / Rank', value = 'Score: ' + str(score) + ' / Popularity: ' + str(pop) + ' / Rank: ' + str(rank), inline = False)
      embed.add_field(name = 'Started Publishing', value = start)
      embed.add_field(name = 'Finished Publishing', value = end)
      embed.add_field(name = 'Synopsis', value = description, inline = False)
      embed.add_field(name = 'Genres', value = genre, inline = False)

      await aio_jikan.close()

      await ctx.send(embed = embed)



  @commands.command()
  async def mangasearch(self, ctx, *, message):
    """Search anime/manga from MyAnimeList.net"""
    aio_jikan = AioJikan()
    
    if message == '':
      await ctx.send('`You need to enter a manga name`')
      return


    if message in UNICODE_EMOJI:
      await ctx.send('`Emjois are not allowed`')
      return 

    async with ctx.channel.typing():

      results = await aio_jikan.search('manga', message)
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
  
  @commands.command(aliases=["user","acc"])
  async def account(self, ctx, message):
    #loop = asyncio.get_event_loop()
    aio_jikan = AioJikan()
    
    if message == '':
      await ctx.send('Well who to search for?')
      return

    async with ctx.channel.typing():

      try:
        user = await aio_jikan.user(username = message)

      except:
        await ctx.send('`User not found`')
        return

      url = user.get('url')
      username = user.get('username')
      anime = user.get('anime_stats')

      if user.get('image_url') == None:
        img = 'https://i.imgur.com/9mnjji8.png'

      else:
        img = user.get('image_url')

      days = anime.get('days_watched')
      avg_score = anime.get('mean_score')
      watching = anime.get('watching')
      completed = anime.get('completed')
      hold = anime.get('on_hold')
      dropped = anime.get('dropped')
      plan = anime.get('plan_to_watch')
      total = anime.get('total_entries')
      num_ep = anime.get('episodes_watched')

      embed = discord.Embed(
        title = '**' + username + '**',
        colour = discord.Color.gold(),
        url = url
      )


      embed.set_thumbnail(url = img)
      embed.add_field(name = 'Days watched', value = days)
      embed.add_field(name = 'Episodes Watched', value = num_ep)
      embed.add_field(name = 'Avg Score', value = avg_score)
      embed.add_field(name = 'Total number of shows', value = total)
      embed.add_field(name = 'Watching', value = watching)
      embed.add_field(name = 'Completed', value = completed)
      embed.add_field(name = 'Plan to Watch', value = plan)
      embed.add_field(name = 'Dropped', value = dropped)
      embed.add_field(name = 'On hold', value = hold)

      await aio_jikan.close()

      await ctx.send(embed = embed)
      return



  @commands.command(aliases=["s","sesn"])
  async def season(self, ctx, year, sesn):
    #loop = asyncio.get_event_loop()
    aio_jikan = AioJikan()

    async with ctx.channel.typing():
      season = await aio_jikan.season(year = int(year), season = sesn)
      anime = season.get('anime')

      embed = discord.Embed(
        title = sesn.capitalize() + ' ' + year + ' Season',
        colour = discord.Color.gold()
      )

      for x in range(5):
        title = anime[x].get('title')
        ep = anime[x].get('episodes')
        score = anime[x].get('score')

        embed.add_field(name = title, value = 'Eps: ' + str(ep) + ' / Score: ' + str(score), inline = False)

      await aio_jikan.close()
      await ctx.send(embed = embed)
    #'anime': is list of shows



  @commands.command(aliases=["sch","time","table"])
  async def schedule(self, ctx, day = ''):
    #loop = asyncio.get_event_loop()
    aio_jikan = AioJikan()

    shows = {
      'm':'monday',
      't':'tuesday',
      'w':'wednesday',
      'r':'thursday',
      'f':'friday',
      's':'saturday',
      'su':'sunday'
    }

    if day == '':
      async with ctx.channel.typing():
        scheduled = await aio_jikan.schedule()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        embed = discord.Embed(
          title = 'Airing',
          colour = discord.Color.gold()
        )

        for x in range(7):
          hr = scheduled.get(days[x])
          date = days[x]
          sch = hr[0]
          title = sch.get('title')
          score = sch.get('score')

          embed.add_field(name = date.capitalize(), value = title + '\nScore: ' + str(score), inline = False)
  

        await ctx.send(embed = embed)
        await aio_jikan.close()
        return

    elif day == 'days':
      async with ctx.channel.typing():
        desc = ''

        for x in shows:
          desc += x + ' : ' + shows[x] + '\n'
          print(desc)

        embed = discord.Embed(
          title = 'Days',
          colour = discord.Color.gold(),
          description = desc
        )
        await ctx.send(embed = embed)
        return

    elif day in shows:
      async with ctx.channel.typing():
        scheduled = await aio_jikan.schedule(shows[day])
    
        embed = discord.Embed(
          title = shows[day].capitalize(),
          colour = discord.Color.gold()
        )

        hr = scheduled.get(shows[day])

        if len(hr) > 7:
          for x in range(7):
            sch = hr[x]
            title = sch.get('title')
            score = sch.get('score')

            embed.add_field(name = title, value = 'Score: ' + str(score), inline = False)

        else:
          for x in range(len(hr)):
            sch = hr[x]
            title = sch.get('title')
            score = sch.get('score')

            embed.add_field(name = title, value = 'Score: ' + str(score), inline = False)

        await ctx.send(embed = embed)
        await aio_jikan.close()
        return

    else:
      await ctx.send('`input a valid day`')
      return

    


  async def fetch(self, session, url):
    async with session.get(url) as response:
      return await response.json()




    
def setup(bot):
    bot.add_cog(MyAnimeList(bot)) 
     
