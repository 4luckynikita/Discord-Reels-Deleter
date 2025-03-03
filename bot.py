import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = int(os.getenv("USER_ID"))

# Get ALLOWED_CHANNEL from .env, default to None if not set. If None is set, bot will block messages within ALL channels!
ALLOWED_CHANNEL = os.getenv("ALLOWED_CHANNEL")
ALLOWED_CHANNEL_ID = int(ALLOWED_CHANNEL) if ALLOWED_CHANNEL else None 

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

# Feel free to tweak this for a different keyword to block
INSTAGRAM_URL = "instagram.com"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.id == TARGET_USER_ID and INSTAGRAM_URL in message.content:
        if ALLOWED_CHANNEL_ID and message.channel.id == ALLOWED_CHANNEL_ID:
            return
        
        try:
            await message.delete()
            await message.channel.send("Nuh uh, no reels in discord #ratio plz send in proper channel 🍊")
        except discord.Forbidden:
            print("Missing permissions to delete messages.")
        except discord.NotFound:
            print("Message already deleted.")

# Jolly ole run command
bot.run(TOKEN)