import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


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
async def on_member_update(before, after):
    # Get the voice client for the voice channel the user is in
    voice_client = after.guild.voice_client

    # Check if the user has joined a voice channel
    if after.channel and voice_client and voice_client.is_connected():
        user_stream = voice_client.source

        # Output the user's audio stream to a separate file
        with open(
            f"user_streams/{after.guild.id}_{after.id}_{after.name}.wav", "wb"
        ) as f:
            async for chunk in user_stream:
                f.write(chunk)


bot.run(TOKEN)
