# Importing necessary modules and classes
import asyncio
# noinspection PyTypeChecker
import re
from abc import ABC, abstractmethod
from decimal import Decimal
import dateutil.parser
import requests
import discord
from forex_python.converter import CurrencyRates
from faker import Faker
import Web_Scrapper_Strategy
import pywhatkit as kit
from PIL import Image, ImageFont, ImageDraw
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch


# Command interface
class Command(ABC):
    @staticmethod
    @abstractmethod
    async def execute(self, ctx, command_name):
        pass


# Concrete command classes for Spotify-related commands
class SpotifyCommands(Command, ABC):
    def __init__(self, bot):
        self.bot = bot

    # Async method to track the current Spotify song
    async def track(ctx):
        receiver = Receiver()
        await receiver.track(ctx)

    # Async method to get an image related to the current Spotify song
    async def track_image(ctx):
        receiver = Receiver()
        await receiver.track_image(ctx)


# Concrete command class for YouTube-related commands
class YoutubeCommands:
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {
            "format": "bestaudio/best",
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": False,
            "yesplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "default_search": "auto",
            "source_address": "0.0.0.0",  # Bind to ipv4 since ipv6 addresses cause issues at certain times
        }
        self.FFMPEG_OPTIONS = {'options': '-vn'}
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    # Async method to search YouTube for a given item
    @staticmethod
    async def search_yt(yt, item):
        receiver = Receiver()
        return await receiver.search_yt(yt, item)

    # Async method to play the next song in the queue
    async def play_next(yt):
        receiver = Receiver()
        await receiver.play_next(yt)

    # Async method to play a specific music item
    @staticmethod
    async def play_music(yt, ctx):
        receiver = Receiver()
        await receiver.play_music(yt, ctx)

    # Async method to play the first song in the queue
    async def play(yt, ctx):
        receiver = Receiver()
        await receiver.play(yt, ctx=ctx)

    # Async method to resume playback
    async def resume(yt, ctx):
        receiver = Receiver()
        await receiver.resume(yt, ctx)

    # Async method to pause playback
    async def pause(yt, ctx):
        receiver = Receiver()
        await receiver.pause(yt, ctx)

    # Async method to skip the current song
    async def skip(yt, ctx):
        receiver = Receiver()
        await receiver.skip(yt, ctx)

    # Async method to display the music queue
    async def queue(yt, ctx):
        receiver = Receiver()
        await receiver.queue(yt, ctx)

    # Async method to leave the voice channel
    async def leave(yt, ctx):
        receiver = Receiver()
        await receiver.leave(yt, ctx)


# Concrete command class for web scraping related commands
class ScrapCommands(Command, ABC):
    async def point_table(ctx):
        receiver = Receiver()
        await receiver.point_table(ctx)


# Concrete command class for League of Legends-related commands
class LolCommands(Command, ABC):
    async def league_scrap(ctx, value, *args):
        receiver = Receiver()
        await receiver.league_scrap(ctx, value, *args)


# Concrete command class for various message-related commands
class MessageCommands(Command, ABC):
    async def hello(ctx):
        receiver = Receiver()
        await receiver.hello(ctx)

    async def finance(ctx, command):
        receiver = Receiver()
        await receiver.finance(ctx, command)

    async def fake(ctx):
        receiver = Receiver()
        await receiver.fake(ctx)

    async def info(ctx, command):
        receiver = Receiver()
        await receiver.info(ctx, command)


class FabricateCommands:

    async def scrap_lol(ctx, command, *args):
        await LolCommands.league_scrap(ctx, command, *args)

    async def scrap_football(ctx):
        await ScrapCommands.point_table(ctx)

    async def spotify_commands(ctx, command_name):
        match command_name:
            case "track":
                await SpotifyCommands.track(ctx)
            case "image":
                await SpotifyCommands.track_image(ctx)
            case _:
                await ctx.send(f"Command '{command_name}' cannot found")

    async def youtube_commands(ctx, command_name, yt):
        match command_name:
            case "play":
                await YoutubeCommands.play(yt, ctx)
            case 'queue':
                await YoutubeCommands.queue(yt, ctx)
            case 'leave':
                await YoutubeCommands.leave(yt, ctx)
            case 'resume':
                await YoutubeCommands.resume(yt, ctx)
            case 'pause':
                await YoutubeCommands.pause(yt, ctx)
            case 'skip':
                await YoutubeCommands.skip(yt, ctx)
            case _:
                await ctx.send(f"Command '{command_name}' cannot found")

    async def hello(ctx):
        await MessageCommands.hello(ctx)

    async def convert(ctx, command):
        await MessageCommands.finance(ctx, command)

    async def fake(ctx):
        await MessageCommands.fake(ctx)

    async def info(ctx, command):
        await MessageCommands.info(ctx, command)


# Concrete class for handling command execution
class Invoker:
    "Invoker class"

    def __init__(self):
        self._commands = {}

    # Registering a command
    def register(self, command_name, command):
        self._commands[command_name] = command

    # Executing a command
    @staticmethod
    async def execute(command_name, ctx, *args):
        await FabricateCommands.fabricate(ctx, command_name)

    @staticmethod
    async def execute_football(ctx):
        await FabricateCommands.scrap_football(ctx)

    @staticmethod
    async def execute_hello(ctx):
        await FabricateCommands.hello(ctx)

    @staticmethod
    async def execute_convert(ctx, command):
        await FabricateCommands.convert(ctx, command)

    @staticmethod
    async def execute_fake(ctx):
        await FabricateCommands.fake(ctx)

    @staticmethod
    async def execute_info(ctx, command):
        await FabricateCommands.info(ctx, command)

    @staticmethod
    async def execute_scrap_lol(ctx, command, *args):
        print(args[0])
        await FabricateCommands.scrap_lol(ctx, command, *args)

    # Executing a YouTube command
    @staticmethod
    async def execute_youtube(ctx, command_name, yt):
        await FabricateCommands.youtube_commands(ctx=ctx, command_name=command_name, yt=yt)

    # Executing a Spotify command
    @staticmethod
    async def execute_spotify(ctx, command_name):
        await FabricateCommands.spotify_commands(ctx, command_name)


# Receiver class containing the actual implementations of commands
class Receiver:
    # Static method to greet the user
    @staticmethod
    async def hello(ctx):
        await ctx.send("Hello")

    # Static method to perform a currency conversion
    @staticmethod
    async def finance(ctx, command):
        currency = re.split(r'(\d+)', command)
        forex = CurrencyRates()
        amount = currency[1]
        from_currency = currency[2]
        to_currency = "TRY"
        price_in_decimal = Decimal(amount.replace(',', '.'))
        result = forex.convert(from_currency.upper(), to_currency, price_in_decimal)
        result = f"{price_in_decimal.quantize(Decimal('0.00'))} {from_currency} = {result.quantize(Decimal('0.00'))} {to_currency}"
        await ctx.send(result)

    # Static method to generate fake identity information
    @staticmethod
    async def fake(ctx):
        fake = Faker()
        embed = discord.Embed(title=f"{fake.name()}",
                              description="Your fake identities",
                              )
        embed.add_field(name="address:", value=fake.address(), inline=False)
        embed.add_field(name="info:", value=str(fake.text()), inline=False)
        embed.add_field(name="email:", value=fake.email(), inline=False)
        embed.add_field(name="country:", value=fake.country(), inline=False)
        embed.add_field(name="latitude:", value=fake.latitude(), inline=False)
        embed.add_field(name="longitude:", value=fake.longitude(), inline=False)
        await ctx.send(embed=embed)

    # Static method to get information about a YouTube video
    @staticmethod
    async def info(ctx, command):
        info = kit.info(command, 100, return_value=True)
        await ctx.send(info)

    # Static method to display the point table of a football league
    @staticmethod
    async def point_table(ctx):
        url = "https://www.livescore.in/tr/futbol/turkiye/super-li-g/#/KzRFDJ4U/table/overall"
        points = Web_Scrapper_Strategy.Context(Web_Scrapper_Strategy.MatchScrapper())
        values, _ = points.run_scrap(url)
        embed = discord.Embed(title="Point Tables Of Super League",
                              url=url,
                              description="This is a point table of Turkish Super League"
                              )
        for i in values:
            embed.add_field(name=f"{i['rank']}{i['team']}",
                            value=f"{i['Match']} Match {i['Win']} Win {i['Lose']} Lose {i['Point']} Point {i['Average']} Average",
                            inline=False)
        embed.set_author(name=ctx.bot.user.display_name, icon_url=ctx.bot.user.display_avatar)
        embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    # Static method to get information about a League of Legends player
    @staticmethod
    async def league_scrap(ctx, value, *args):

        try:
            league = Web_Scrapper_Strategy.Context(Web_Scrapper_Strategy.RiotScrapper())
            value, url = league.run_scrap(value, *args)
            embed = discord.Embed(title=f"{value[0]['rank'].capitalize()}",
                                  description=f"Win:{value[0]['win']} Winrate:{value[0]['win-rate']}%",
                                  )
            embed.set_thumbnail(url=value[0]['rank_img'])
            embed.set_author(name=f"{value[0]['user']}#{value[0]['server']}", icon_url=value[0]['profile_img'], url=url)
            embed.set_footer(text=f"Information requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        except:
            await ctx.send("User not found or User is unranked")

    # Static method to search for a YouTube video and return its details
    @staticmethod
    async def search_yt(yt, item):
        if item.startswith("https://"):
            title = yt.ytdl.extract_info(item, download=False)["title"]
            return {'source': item, 'title': title}
        search = VideosSearch(item, limit=1)
        return {'source': search.result()["result"][0]["link"], 'title': search.result()["result"][0]["title"]}

    # Static method to play the next song in the queue
    @staticmethod
    async def play_next(yt):
        before_option = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                         'options': '-vn'}
        if len(yt.music_queue) > 0:
            yt.is_playing = True
            m_url = yt.music_queue[0][0]['source']
            yt.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: yt.ytdl.extract_info(m_url, download=False))
            song = data['url']
            yt.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **yt.FFMPEG_OPTIONS, before_option=before_option),
                       after=lambda e: asyncio.run_coroutine_threadsafe(yt.play_next(), yt.bot.loop))
        else:
            yt.is_playing = False

    # Static method to play a specific music item
    @staticmethod
    async def play_music(yt, ctx):
        before_option = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                         'options': '-vn'}
        if len(yt.music_queue) > 0:
            yt.is_playing = True
            m_url = yt.music_queue[0][0]['source']
            if yt.vc is None or not yt.vc.is_connected():
                yt.vc = await yt.music_queue[0][1].connect()
                if yt.vc is None:
                    await ctx.send("```Could not connect to the voice channel```")
                    return
            else:
                await yt.vc.move_to(yt.music_queue[0][1])
            yt.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: yt.ytdl.extract_info(m_url, download=False))
            song = data['url']
            yt.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **yt.FFMPEG_OPTIONS, before_options=before_option),
                       after=lambda e: asyncio.run_coroutine_threadsafe(yt.play_next(), yt.bot.loop))
        else:
            yt.is_playing = False

    # Static method to play a YouTube video
    @staticmethod
    async def play(yt, ctx, *args):
        query = "".join(ctx.args[1])
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.send("```You need to connect to a voice channel first!```")
            return
        if yt.is_paused:
            yt.vc.resume()
        else:
            song = await yt.search_yt(yt, query)
            if type(song) == type(True):
                await ctx.send(
                    "```Could not download the song. Incorrect format try another keyword. This could be due to "
                    "playlist or a livestream format.```")
            else:
                if yt.is_playing:
                    await ctx.send(f"**#{len(yt.music_queue) + 2} -'{song['title']}'** added to the queue")
                else:
                    await ctx.send(f"**'{song['title']}'** added to the queue")
                yt.music_queue.append([song, voice_channel])
                if not yt.is_playing:
                    await yt.play_music(yt, ctx)

    # Static method to pause playback
    @staticmethod
    async def pause(yt, ctx, *args):
        if yt.is_playing:
            yt.is_playing = False
            yt.is_paused = True
            yt.vc.pause()

        elif yt.is_paused:
            yt.vc.resume()

    # Static method to resume playback
    @staticmethod
    async def resume(yt, ctx, *args):
        if yt.is_paused:
            yt.is_playing = True
            yt.is_paused = False
            yt.vc.resume()

    # Static method to skip the current song
    @staticmethod
    async def skip(yt, ctx, *args):
        if yt.vc is not None and yt.vc:
            yt.vc.stop()
            await yt.play_music(yt,ctx)

    # Static method to display the music queue
    @staticmethod
    async def queue(yt, ctx):
        retval = ""
        for i in range(len(yt.music_queue)):
            if i > 4: break
            retval += yt.music_queue[i][0]['title'] + '\n'
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in the queue")

    # Static method to leave the voice channel
    @staticmethod
    async def leave(yt, ctx):
        yt.is_playing = False
        yt.is_paused = False
        yt.music_queue = []
        await yt.vc.disconnect()

    # Static method to track the Spotify activity of a user
    @staticmethod
    async def track(ctx, user: discord.Member = None):
        user = user or ctx.author

        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

        if spotify_result is None:
            await ctx.send(f"{user.name} is not listening to Spotify")

        await ctx.send(f"https://open.spotify.com/track/{spotify_result.track_id}")

    # Static method to track the Spotify activity of a user but with image
    @staticmethod
    async def track_image(ctx, user: discord.Member = None):
        user = user or ctx.author

        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

        if spotify_result is None:
            await ctx.send(f"{user.name} is not listening to Spotify")

        # await ctx.send(f"https://open.spotify.com/track/{spotify_result.track_id}")

        # Images
        track_background_image = Image.open('.assets\\spotify_template.png')
        album_image = Image.open(requests.get(spotify_result.album_cover_url, stream=True).raw).convert("RGBA")

        # Font
        title_font = ImageFont.truetype('theboldfont.ttf', size=16)
        artist_font = ImageFont.truetype('theboldfont.ttf', size=14)
        album_font = ImageFont.truetype('theboldfont.ttf', size=14)
        start_duration_font = ImageFont.truetype('theboldfont.ttf', size=12)
        end_duration_font = ImageFont.truetype('theboldfont.ttf', size=12)

        # Position
        title_text_positon = 150, 30
        artist_text_positon = 150, 60
        album_text_positon = 150, 80
        start_duration_text_positon = 150, 122
        end_duration_text_positon = 515, 123

        # Draw
        date = dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')

        draw_on_image = ImageDraw.Draw(track_background_image)
        draw_on_image.text(title_text_positon, spotify_result.title, 'white', font=title_font)
        draw_on_image.text(artist_text_positon, f' by {spotify_result.artist}', 'white', font=artist_font)
        draw_on_image.text(album_text_positon, spotify_result.album, 'white', font=album_font)
        draw_on_image.text(start_duration_text_positon, '0.00', 'white', font=start_duration_font)
        draw_on_image.text(end_duration_text_positon, f'{date}', 'white', font=end_duration_font)

        # Background Color
        album_color = album_image.getpixel((250, 100))
        back_ground_image_color = Image.new('RGBA', track_background_image.size, album_color)
        back_ground_image_color.paste(track_background_image, (0, 0), track_background_image)

        # Resize
        album_image_resize = album_image.resize((140, 160))
        back_ground_image_color.paste(album_image_resize, (0, 0), album_image_resize)

        # Save Image
        back_ground_image_color.convert('RGB').save('spotify.jpg', 'JPEG')

        await ctx.send(file=discord.File('spotify.jpg'))