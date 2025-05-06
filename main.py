
import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
import datetime
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 환경 설정 (필요에 따라 직접 설정)
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
WELCOME_CHANNEL_ID = 123456789012345678
CLASS_CHANGE_CHANNEL_ID = 123456789012345678
BOT_NOTIFY_CHANNEL_ID = 123456789012345678
EVENT_CHANNEL_ID = 123456789012345678
CHAT_CHANNEL_ID = 123456789012345678
NOTICE_CHANNEL_ID = 123456789012345678

ROLE_IDS = {
    "T1-T3": 111111111111111111,
    "T4": 222222222222222222,
    "manager": 333333333333333333,
    "Korean": 444444444444444444,
    "English": 555555555555555555
}

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    channel = bot.get_channel(BOT_NOTIFY_CHANNEL_ID)
    if channel:
        await channel.send("영이 봇 2.0ver 준비 완료! 뭐든 시켜줘")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(
            f"**{member.mention}님**, 환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

"
            "1. 서버에 역할이 존재합니다! `/!역할/`, `/!국가/` 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
"
            "2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
"
            "3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!

"
            "**ENGLISH**
"
            "1. A role exists on the server! Enter `/!class/`, `/!country/` in the chat to create a choice After you select, you are granted access to the channel!
"
            "2. For mutual prevention of quarrels, please check the rules in the Notice-Rules to recognize simple rules and use them!
"
            "3. If you need additional server extensions or are limited in use, please contact your server administrator or executive if you need any services!"
        )

@bot.command(name="명령어")
async def 명령어(ctx):
    await ctx.send("사용 가능한 명령어: `!역할`, `!class`, `!국가`, `!country`, `!명령어`, `!command`, `!청소`, `!통계`, `!영이`")

@bot.command(name="command")
async def command(ctx):
    await 명령어(ctx)

@bot.command(name="영이")
async def 영이(ctx):
    quotes = [
        "오늘도 좋은 하루~",
        "난 봇이지만 널 응원해!",
        "점심 뭐 먹을까?",
        "코딩 너무 재밌지 않니?",
        "나는 영이 봇이야!"
    ]
    await ctx.send(random.choice(quotes))

@bot.command(name="청소")
async def 청소(ctx):
    if any(role.id in [ROLE_IDS["T4"], ROLE_IDS["manager"]] for role in ctx.author.roles):
        await ctx.channel.purge(limit=5)
        await ctx.send("최근 메시지 5개를 삭제했어요.", delete_after=3)
    else:
        await ctx.send("이 명령어는 관리자만 사용할 수 있어요.", delete_after=5)

@bot.command(name="class")
async def class_command(ctx):
    await 역할(ctx)

@bot.command(name="country")
async def country_command(ctx):
    await 국가(ctx)

@bot.command(name="역할")
async def 역할(ctx):
    await ctx.send("역할 선택: (T1~T3), (T4), (Manager)")

@bot.command(name="국가")
async def 국가(ctx):
    await ctx.send("국가 선택: (Korean), (English)")

@tasks.loop(minutes=1)
async def schedule_check():
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    if now.strftime("%Y-%m-%d %H:%M") == "2025-07-04 09:00":
        channel = bot.get_channel(EVENT_CHANNEL_ID)
        if channel:
            await channel.send("꼬마전사 전역 축하해!!! 이제 일해서 과금해!!")

@bot.event
async def on_message(message):
    if message.channel.id == NOTICE_CHANNEL_ID and message.author != bot.user:
        await message.channel.send("다들 빨리확인해요 중요한거에요")
    await bot.process_commands(message)

keep_alive()
bot.run(TOKEN)
