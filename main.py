import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="👋🏼환영합니다👋🏼")
    if channel:
        welcome_message = (
            "환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!\n\n"
            "1. 서버에 역할이 존재합니다! `/!역할/`, `/!국가/` 을 채팅에 입력하면 선택지가 생성됩니다. 선택 후 채널 입장 권한이 부여됩니다!\n"
            "2. 상호간에 다툼 방지를 위해서 간단한 규칙을 인지하기 위해 `공지-규칙`에서 규칙을 확인 후 이용 바랍니다!\n"
            "3. 추가적인 서버 증설이 필요하거나 이용이 제한됨, 필요한 서비스가 있을 시 서버 관리자 혹은 임원에게 문의해주세요!\n\n"
            "**Welcome!! Here's a quick introduction to the server!**\n\n"
            "1. A role exists on the server! Type `/!Role/`, `/!Country/` in the chat to see the choices. Once selected, you'll be granted access to channels!\n"
            "2. To prevent conflicts, please check the rules in the `Notice-Rules` channel before using the server.\n"
            "3. If you need additional server features or have limitations, please contact the admin or an executive!"
        )
        await channel.send(welcome_message)

bot.run("YOUR_DISCORD_BOT_TOKEN")
