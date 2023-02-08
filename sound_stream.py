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


@bot.command(name="leave", help="Leaves a voice channel")
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_member_update(self, member, before, after):
    # Get the voice client for the voice channel the user is in
    voice_client = discord.utils.get(self.voice_clients, guild=member.guild)

    # Check if the user has joined a voice channel
    if after.channel and voice_client and voice_client.is_connected():
        user_stream = voice_client.source

        # Output the user's audio stream to a separate file
        with open(f"{member.id}_{member.name}.wav", "wb") as f:
            async for chunk in user_stream:
                f.write(chunk)
