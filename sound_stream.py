import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(name="join", help="Joins a voice channel")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
