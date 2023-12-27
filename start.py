import discord
from bot_connection import BotConnection
from commands_pattern import Invoker, FabricateCommands, YoutubeCommands, SpotifyCommands, LolCommands

# Configuring Discord intents to enable specific events
intents = discord.Intents.default()
intents.message_content = True

# Creating an instance of BotConnection
bot_connection = BotConnection()

# Retrieving the Discord bot and token
bot, token = bot_connection.bot_connection()

# Creating an instance of the command invoker
invoker = Invoker()

# Creating an instance of YoutubeCommands and adding it as a Discord cog
yt = YoutubeCommands(bot)
bot.add_cog(yt)


# Command to invoke custom commands using the invoker
@bot.command(name="points")
async def invoke_command(ctx):
    invoker.register("points", FabricateCommands)
    await invoker.execute_football(ctx)


@bot.command(name="lol")
async def invoke_command(ctx, command_name, *args):
    await ctx.send(f"Looking player {command_name}")
    invoker.register(command_name, LolCommands)
    await invoker.execute_scrap_lol(ctx, command_name, *args)


@bot.command(name="hello")
async def invoke_command(ctx):
    invoker.register("hello", FabricateCommands)
    await invoker.execute_hello(ctx)


@bot.command(name="convert")
async def invoke_command(ctx, command_name, *args):
    invoker.register(command_name, FabricateCommands)
    await invoker.execute_convert(ctx, command_name)


@bot.command(name="fake")
async def invoke_command(ctx):
    invoker.register("fake", FabricateCommands)
    await invoker.execute_fake(ctx)


@bot.command(name="info")
async def invoke_command(ctx, command_name):
    invoker.register(command_name, FabricateCommands)
    await invoker.execute_info(ctx, command_name)


# Command to play a song from Youtube
@bot.command(name="play", aliases=['p', 'playing'], help="Play the selected song from Youtube")
async def invoke_youtube(ctx, *args):
    invoker.register("play", YoutubeCommands)
    await invoker.execute_youtube(ctx=ctx, command_name="play", yt=yt)


# Command to display the current music queue
@bot.command(name="queue")
async def invoke_queue(ctx):
    invoker.register("queue", YoutubeCommands)
    await invoker.execute_youtube(ctx=ctx, command_name="queue", yt=yt)


# Command to resume playing music
@bot.command(name="resume")
async def invoke_resume(ctx):
    invoker.register("resume", YoutubeCommands)
    await invoker.execute_youtube(ctx=ctx, command_name="resume", yt=yt)


# Command to pause playing music
@bot.command(name="pause")
async def invoke_pause(ctx):
    invoker.register("pause", YoutubeCommands)
    await invoker.execute_youtube(ctx=ctx, command_name="pause", yt=yt)


# Command to skip to the next song
@bot.command(name="skip")
async def invoke_skip(ctx):
    invoker.register("skip", YoutubeCommands)
    await invoker.execute_youtube(ctx=ctx, command_name="skip", yt=yt)


# Command to make the bot leave the voice channel
@bot.command(name="leave")
async def invoke_leave(ctx):
    invoker.register("leave", YoutubeCommands)
    await invoker.execute_youtube(ctx=ctx, command_name="leave", yt=yt)


# Command to invoke Spotify commands
@bot.command(name="spotify")
async def invoke_spotify(ctx, command_name):
    invoker.register(command_name, SpotifyCommands)
    await invoker.execute_spotify(ctx, command_name)


# Running the bot
bot.run(token)
