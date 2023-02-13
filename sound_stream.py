import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from stream_recorder import StreamRecorder


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


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
async def on_voice_state_update(member, before, after):
    # Get the voice client for the voice channel the user is in
    voice_client = after.channel.guild.voice_client

    # Check if the user has joined a voice channel
    if after.channel and voice_client:
        user_stream = StreamRecorder(
            voice_client,
            member,
            file_path=f"user_streams/{member.guild.id}_{member.id}_{member.name}.wav",
        )
        await user_stream.start()

        await asyncio.sleep(5)

        await user_stream.stop()


bot.run(TOKEN)
