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

# Load blocked terms from blocked_terms.txt
BLOCKED_TERMS_FILE = "blocked_terms.txt"

def load_blocked_terms(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. No blocked terms loaded.")
        return []

def add_blocked_term(term):
    term = term.lower().strip()
    if term and term not in blockedTerms:
        with open(BLOCKED_TERMS_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{term}")  # Ensure new terms are added on a new line
        blockedTerms.append(term)
        return True
    return False
def remove_blocked_term(term):
    term = term.lower().strip()
    if term in blockedTerms:
        blockedTerms.remove(term)
        try:
            with open(BLOCKED_TERMS_FILE, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]  # Strip whitespace and newlines

            # Write back only terms that are not removed and not empty
            with open(BLOCKED_TERMS_FILE, "w", encoding="utf-8") as f:
                f.writelines(f"{line}\n" for line in lines if line and line.lower() != term)

            return True
        except Exception as e:
            print(f"Error removing term: {e}")
            return False
    return False

blockedTerms = load_blocked_terms(BLOCKED_TERMS_FILE)
blockedTermResponse = os.getenv("BLOCKED_TERM_RESPONSE", "Your message contains a blocked term!")

# Helper function to check if one array contains a value out of another array, not case sensitive
def check_common_term(arr1, arr2):
    set2 = set(arr2)  # Convert to set for faster lookups
    return any(str(element).lower() in set2 for element in arr1)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Feel free to tweak this for a different keyword to block
INSTAGRAM_URL = "instagram.com"

@tree.command(name="blockterm", description="Block a new term by adding it to the list.")
async def blockterm(interaction: discord.Interaction, term: str):
    if add_blocked_term(term):
        await interaction.response.send_message(f"Term `{term}` is no more. 🚫")
    else:
        await interaction.response.send_message(f"Term `{term}` is already blocked or invalid.", ephemeral=True)

@tree.command(name="unblockterm", description="Remove a term from the blocked list.")
async def unblockterm(interaction: discord.Interaction, term: str):
    if remove_blocked_term(term):
        await interaction.response.send_message(f"Term `{term}` has been unblocked. ✅")
    else:
        await interaction.response.send_message(f"Term `{term}` was not found in the list.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Blocked terms loaded:")
    for term in blockedTerms:
        print(term)
    print(f"Blocked term response: {blockedTermResponse}")

    try:
        await tree.sync()  # Sync slash commands
        print("Slash commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if check_common_term(message.content.split(' '), blockedTerms):
        try:
            await message.channel.send(blockedTermResponse)
        except discord.Forbidden:
            print("Missing permissions to send messages.")

    if message.author.id == TARGET_USER_ID and INSTAGRAM_URL in message.content:
        if ALLOWED_CHANNEL_ID and message.channel.id == ALLOWED_CHANNEL_ID:
            return
        
        try:
            await message.delete()
            await message.channel.send("Nuh uh, no reels in discord #ratio plz send in proper channel 🍊")
        except discord.Forbidden:
            print("Missing permissions to send or delete messages.")
        except discord.NotFound:
            print("Message already deleted.")

# Jolly ole run command
bot.run(TOKEN)