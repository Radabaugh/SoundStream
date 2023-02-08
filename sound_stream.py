import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(name="join", help="Joins a voice channel")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(
    name="leave",
    help="Leaves a voice channel and deletes audio files created by the bot",
)
async def leave(ctx):
    voice_client = ctx.guild.voice_client

    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()

        # Delete all audio files created by the bot
        path = os.path.join(os.getcwd(), "user_streams")

        for file in os.listdir(path):
            if file.startswith(str(ctx.guild.id)):
                os.remove(file)


@bot.event
async def on_member_update(self, member, before, after):
    # Get the voice client for the voice channel the user is in
    voice_client = discord.utils.get(self.voice_clients, guild=member.guild)

    # Check if the user has joined a voice channel
    if after.channel and voice_client and voice_client.is_connected():
        user_stream = voice_client.source

        # Output the user's audio stream to a separate file
        with open(
            f"user_streams/{member.guild.id}_{member.id}_{member.name}.wav", "wb"
        ) as f:
            async for chunk in user_stream:
                f.write(chunk)


bot.run(TOKEN)
