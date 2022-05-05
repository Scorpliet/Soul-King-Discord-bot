import asyncio
import functools
import itertools
import math
import random
import urllib
import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
import re
#import pafy
import os
token = os.environ.get("YAPIV3")
from urllib.parse import parse_qs, urlparse
#pafy.set_api_key(token)
import googleapiclient.discovery


youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'yesplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -probesize 15000000',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 1):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)
    
    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = functools.partial(cls.ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{}h'.format(hours))
        if minutes > 0:
            duration.append('{}m'.format(minutes))
        if seconds > 0:
            duration.append('{}s'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title=':dvd: {0.source.title} :dvd:'.format(self),  color=discord.Color.gold())
                 .add_field(name='\u200d', value=f'**Duration** {self.source.duration} \n**Artist** [{self.source.uploader}]({self.source.uploader_url}) \n**Added by** {self.requester.mention}', inline = True)
                 #.add_field(name='<:user:804063696799662101> Requested by', value=self.requester.mention, inline = True)
                 #.add_field(name='<:artist:804063511470800916> Artist', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))
        #embed.thumbnail(width=256, height=200)
        #embed.set_image(url=self.souce.thumbnail)         

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]
   

    def history(self):
        if not self._queue:
            pass

        return self._queue[:self.position]

class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()
        self.exists = True
        self._loop = False
        self._volume = 1
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if self.loop == False:
                try:
                    async with timeout(86400):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    self.exists= False
                    return
                #if not isinstance(self.current, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                  #try:
                    #self.current = await YTDLSource.regather_stream(self.current, loop=self.bot.loop)
                  #except Exception as e:
                    #await self._channel.send(f':notes: There was an error processing your song.\n'
                                             #f'```css\n[{e}]\n```')
                   # continue
                self.current.source.volume = self._volume
                self.voice.play(self.current.source, after=self.play_next_song)
                await self.current.source.channel.send(embed=self.current.create_embed())

            elif self.loop == True:
                self.now = discord.FFmpegPCMAudio(self.current.source.stream_url, **YTDLSource.FFMPEG_OPTIONS)
                self.voice.play(self.now, after=self.play_next_song)    

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}


    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Loaded")


    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state or not state.exists:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)          

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        
        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            em = discord.Embed(title=f":zzz: Summoned in {destination}", description = "What? tf, why i'm here.", color = ctx.author.color)
            em.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        
        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect','dis'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')
        await ctx.message.add_reaction('👋')
        #dest = ctx.author.voice.channel
        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

# Search whatever u want on youtube!
    @commands.command()
    async def syt(self, ctx, *, search):

        
        query_string = urllib.parse.urlencode({
                "search_query": search
        })
        html_content = urllib.request.urlopen(
            "http://youtube.com/results?" + query_string
        )
    
        search_content = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
        em = discord.Embed(title = ":bulb: **Search Result**", description = "http://youtube.com/watch?v=" + search_content[0], color = ctx.author.color)
        em.set_thumbnail(url="https://yt3.ggpht.com/ytc/AAUvwnhRCS00s226UbsoI2uhe2XFedXEIBw9jaOtstvTo08=s900-c-k-c0x00ffffff-no-rj")
        em.set_footer(text=f"Search requested by {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=em)
        

    @commands.command(name='volume', aliases=['vol', 'v'])
    async def _volume(self, ctx: commands.Context, *, volume: int):

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if volume > 100:
            return await ctx.send(':x: Volume must be between **0 and 100**')

        ctx.voice_client.source.volume = volume / 100
        em = discord.Embed(title=":sound: Volume settings!", description = 'Volume regulated at {}%'.format(volume), color = ctx.author.color)
        em.set_footer(text=f"Regulated by {ctx.author.name}")    
        await ctx.send(embed=em)

    @commands.command(name='now', aliases=['current', 'playing', 'np'])
    async def _now(self, ctx: commands.Context):

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause', aliases=['pau'])
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume', aliases=['res'])
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name="stop")
    async def _stop(self, ctx):
      ctx.voice_state.songs.clear()
      if ctx.voice_state.is_playing:
        ctx.voice_state.voice.stop()
        await ctx.message.add_reaction('⏹')
        #voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        #voice.stop()

    @commands.command(name='skip', aliases=['next', 'n'])
    async def _skip(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue', aliases=['q'])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('The queue is empty.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} Tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue), color=discord.Color.gold())
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle', aliases=['sh'])
    async def _shuffle(self, ctx: commands.Context):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove', aliases=['rem', 'pop'])
    async def _remove(self, ctx: commands.Context, index: int):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop', aliases=['repeat', 'l'])
    async def _loop(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    
    @commands.command(name='playlist', aliases=['pl'])
    async def _playlist(self, ctx: commands.Context, url:str):
     if not ctx.voice_state.voice:
            await ctx.invoke(self._join)
     query = parse_qs(urlparse(url).query, keep_blank_values=True)
     playlist_id = query["list"][0]


     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = token)

     request = youtube.playlistItems().list(
     part = "snippet",
     playlistId = playlist_id,
     maxResults = 10)
     response = request.execute()

     playlist_items = []
     while request is not None:
       response = request.execute()
       playlist_items += response["items"]
       request = youtube.playlistItems().list_next(request, response)
     videos = []
     for t in playlist_items:
       videos.append(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}')  
     async with ctx.typing():
             try:
                source = await YTDLSource.create_source(ctx, videos[0], loop=self.bot.loop)
             except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e))) 
     for i in videos:
                   try: 
                     source = await YTDLSource.create_source(ctx, i, loop=self.bot.loop)
                     song = Song(source)
                     await ctx.voice_state.songs.put(song)
                   except Exception:
                     continue
     await ctx.send(':headphones: Enqueued {} tracks'.format(len(videos)))           

    @commands.command(name='play', aliases=['p'])
    async def _play(self, ctx: commands.Context, *, search: str):
      """Play anything from youtube, including playlists"""
      if not ctx.voice_state.voice:
            await ctx.invoke(self._join)
                 
      if "playlist?list=" in search or "&list=" in search and "&index" not in search:
        query = parse_qs(urlparse(search).query, keep_blank_values=True)
        playlist_id = query["list"][0]
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = token)

        request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 10,)
        response = request.execute()
        playlist_title = response["items"][0]["snippet"]["title"]
        playlist_items = []
        while request is not None:
           response = request.execute()
           playlist_items += response["items"]
           request = youtube.playlistItems().list_next(request, response)
        videos = []
        for t in playlist_items:
          videos.append(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}')  
        async with ctx.typing():
             try:
                source = await YTDLSource.create_source(ctx, videos[0], loop=self.bot.loop)
             except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e))) 
        for i in videos:
              try: 
                source = await YTDLSource.create_source(ctx, i, loop=self.bot.loop)
                song = Song(source)
                await ctx.voice_state.songs.put(song)
              except Exception:
                continue
        await ctx.send(f':headphones: Enqueued **{len(videos)}** tracks from playlist **{playlist_title}**')   
      
      else: 
        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except Exception as e:
                #youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = token)
                #req=youtube.search().list(q=search, part="snippet")
                #res=req.execute()
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send(':headphones: Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
    @commands.command(name="previous")
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            await ctx.send("Nothing in queue")
            return

        player.queue.position -= 2
        await player.stop()
        await ctx.send("Playing previous track in queue.")

def setup(bot):
    bot.add_cog(music(bot))
