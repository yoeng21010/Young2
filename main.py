import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def 도움말(ctx):
    await ctx.send("사용 가능한 명령어는 다음과 같습니다:\n!역할\n!국가")

TOKEN = "YOUR_BOT_TOKEN"
bot.run(TOKEN)
