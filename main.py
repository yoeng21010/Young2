# main.py - Young2Bot 2.0 with additional features
from keep_alive import keep_alive
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import pytz
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(YOUR_BOT_CHANNEL_ID)
    if channel:
        await channel.send("영이 봇 2.0ver 준비 완료! 뭐든 시켜줘")

@bot.command()
async def 역할(ctx):
    await ctx.send("역할 버튼 선택지")  # 버튼 코드 생략

@bot.command()
async def class_(ctx):
    await 역할(ctx)

@bot.command()
async def 국가(ctx):
    await ctx.send("국가 버튼 선택지")  # 버튼 코드 생략

@bot.command()
async def country(ctx):
    await 국가(ctx)

@bot.command()
async def 명령어(ctx):
    await ctx.send("사용 가능한 명령어: !역할, !class, !국가, !country, !명령어, !command, !청소, !통계, !영이")

@bot.command()
async def command(ctx):
    await 명령어(ctx)

@bot.command()
@commands.has_any_role('manager', 'T4')
async def 청소(ctx, count: int = 5):
    await ctx.channel.purge(limit=count+1)
    await ctx.send(f"{count}개의 메시지를 삭제했어요!", delete_after=5)

@bot.command()
@commands.has_any_role('manager', 'T4')
async def 통계(ctx):
    await ctx.send("통계 기능은 개발 중입니다.")

@bot.command()
async def 영이(ctx):
    import random
    jokes = [
        "나 요즘 코딩만 해... 자괴감이 들어!",
        "디버깅은 나의 삶이야.",
        "영이 봇은 귀엽지 않나요?",
        "누가 내 소스코드 수정했어?",
        "버튼 누르면 뭐가 나올까요~?"
    ]
    await ctx.send(random.choice(jokes))

@bot.event
async def on_message(message):
    if message.channel.id == YOUR_NOTICE_CHANNEL_ID and message.author != bot.user:
        await message.channel.send("다들 빨리확인해요 중요한거에요")
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(YOUR_WELCOME_CHANNEL_ID)
    if welcome_channel:
        await welcome_channel.send("""환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!

1. A role exists on the server! Enter /!class/, /!country/ in the chat to create a choice After you select, you are granted access to the channel!
2. For mutual prevention of quarrels, please check the rules in the Notice-Rules to recognize simple rules and use them!
3. If you need additional server extensions or are limited in use, please contact your server administrator or executive if you need any services!
""")

# Time-based message (Run in background)
async def scheduled_events():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.now(pytz.timezone("Asia/Seoul"))
        if now.strftime('%A') == 'Saturday' and now.hour == 9 and now.minute == 0:
            channel = bot.get_channel(YOUR_CHAT_CHANNEL_ID)
            if channel:
                await channel.send("즐거운 주말이에요! 다들 라오킹접속해서 일일보상 챙겨!!")
        elif now.strftime('%A') == 'Sunday' and now.hour == 21 and now.minute == 0:
            channel = bot.get_channel(YOUR_CHAT_CHANNEL_ID)
            if channel:
                await channel.send("다들 주말동안 잘쉬었어? 내일은 일하러 가야하니까 다들 일찍 자 고생해!!")
        elif now.strftime('%Y-%m-%d %H:%M') == '2025-07-04 09:00':
            channel = bot.get_channel(YOUR_EVENT_CHANNEL_ID)
            if channel:
                await channel.send("꼬마전사 전역 축하해!!! 이제 일해서 과금해!!")
        await asyncio.sleep(60)

asyncio.create_task(scheduled_events())

keep_alive()
bot.run(os.getenv("TOKEN"))
