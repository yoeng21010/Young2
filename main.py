
import discord
from discord.ext import commands
import asyncio
import datetime
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
WELCOME_CHANNEL_ID = 123456789012345678  # replace with your welcome channel ID
CLASS_CHANGE_CHANNEL_ID = 123456789012345678  # replace with class change notification channel ID
BOT_NOTIFY_CHANNEL_ID = 123456789012345678  # replace with bot status notify channel ID
EVENT_CHANNEL_ID = 123456789012345678  # replace with event announcement channel ID
CHAT_CHANNEL_ID = 123456789012345678  # replace with scheduled chat message channel ID
NOTICE_CHANNEL_ID = 123456789012345678  # replace with notice channel ID

ROLE_IDS = {
    "T1-T3": 111111111111111111,
    "T4": 222222222222222222,
    "manager": 333333333333333333,
    "Korean": 444444444444444444,
    "English": 555555555555555555
}

class MyBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(scheduled_events())

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    channel = bot.get_channel(BOT_NOTIFY_CHANNEL_ID)
    if channel:
        await channel.send("영이 봇 2.0ver 준비 완료! 뭐든 시켜줘")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        welcome_msg = '''환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!

1. A role exists on the server! Enter /!class/, /!country/ in the chat to create a choice After you select, you are granted access to the channel!
2. For mutual prevention of quarrels, please check the rules in the Notice-Rules to recognize simple rules and use them!
3. If you need additional server extensions or are limited in use, please contact your server administrator or executive if you need any services!
'''
        await channel.send(welcome_msg)

@bot.command(name='역할', aliases=['class'])
async def role_cmd(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="T1~T3", style=discord.ButtonStyle.primary, custom_id="role_T1-T3"))
    view.add_item(discord.ui.Button(label="T4", style=discord.ButtonStyle.secondary, custom_id="role_T4"))
    view.add_item(discord.ui.Button(label="Manager", style=discord.ButtonStyle.success, custom_id="role_manager"))
    await ctx.send("역할을 선택하세요!", view=view)

@bot.command(name='국가', aliases=['country'])
async def country_cmd(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="한국어", style=discord.ButtonStyle.primary, custom_id="nation_Korean"))
    view.add_item(discord.ui.Button(label="English", style=discord.ButtonStyle.secondary, custom_id="nation_English"))
    await ctx.send("국가를 선택하세요!", view=view)

@bot.command(name='명령어', aliases=['command'])
async def command_list(ctx):
    msg = "**[사용 가능한 명령어 목록]**\n!역할, !class, !국가, !country, !명령어, !command, !청소, !통계, !영이"
    await ctx.send(msg)

@bot.command(name='청소')
async def clean(ctx):
    if any(role.name in ["T4", "manager"] for role in ctx.author.roles):
        await ctx.channel.purge(limit=5)
        await ctx.send("최근 메시지 5개를 삭제했어요!", delete_after=3)
    else:
        await ctx.send("권한이 없습니다!", delete_after=3)

@bot.command(name='영이')
async def random_msg(ctx):
    import random
    messages = [
        "나는 영이 봇! 세상에서 제일 귀엽지!",
        "영이 봇이 지켜보고 있어요...",
        "오늘도 멋진 하루 되세요!",
        "영이는 커피 좋아해요!",
        "버그 신고는 하지 마세요... 농담이에요!"
    ]
    await ctx.send(random.choice(messages))

# 버튼 처리
@bot.event
async def on_interaction(interaction):
    cid = interaction.data.get("custom_id")
    member = interaction.user
    role_name = None

    if cid == "role_T1-T3":
        role_name = "T1-T3"
    elif cid == "role_T4":
        role_name = "T1-T3"
        notify = bot.get_channel(CLASS_CHANGE_CHANNEL_ID)
        if notify:
            await notify.send(f"{member.name}님이 T4 역할을 신청했습니다.")
    elif cid == "role_manager":
        role_name = "T1-T3"
        notify = bot.get_channel(CLASS_CHANGE_CHANNEL_ID)
        if notify:
            await notify.send(f"{member.name}님이 관리자 역할을 신청했습니다.")
    elif cid == "nation_Korean":
        role_name = "Korean"
    elif cid == "nation_English":
        role_name = "English"

    if role_name:
        role = discord.utils.get(member.guild.roles, id=ROLE_IDS[role_name])
        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"{role.name} 역할이 부여되었습니다!", ephemeral=True)

# 공지 감지
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.channel.id == NOTICE_CHANNEL_ID and message.author != bot.user:
        await message.channel.send("다들 빨리확인해요 중요한거에요")

# 스케줄 이벤트
async def scheduled_events():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        if now.weekday() == 5 and now.hour == 9 and now.minute == 0:
            ch = bot.get_channel(CHAT_CHANNEL_ID)
            if ch:
                await ch.send("즐거운 주말이에요! 다들 라오킹 접속해서 일일보상 챙겨!!")
        if now.weekday() == 6 and now.hour == 21 and now.minute == 0:
            ch = bot.get_channel(CHAT_CHANNEL_ID)
            if ch:
                await ch.send("다들 주말동안 잘쉬었어? 내일은 일하러 가야하니까 다들 일찍 자 고생해!!")
        if now.month == 7 and now.day == 4 and now.hour == 9 and now.minute == 0:
            ch = bot.get_channel(EVENT_CHANNEL_ID)
            if ch:
                await ch.send("꼬마전사 전역 축하해!!! 이제 일해서 과금해!! 🎉")
        await asyncio.sleep(60)

keep_alive()
bot.run(TOKEN)
