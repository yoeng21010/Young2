import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

keep_alive()
bot.run(os.getenv("TOKEN"))
