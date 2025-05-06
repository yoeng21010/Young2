
# 디스코드 봇 메인 코드 (영이봇 2.0)
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
from datetime import datetime
import pytz
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 환경변수에서 토큰 로딩
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_CHANNEL_ID = int(os.getenv("ctx.channel.send()"))
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))
NOTICE_CHANNEL_ID = int(os.getenv("NOTICE_CHANNEL_ID"))
EVENT_CHANNEL_ID = int(os.getenv("EVENT_CHANNEL_ID"))
CHAT_CHANNEL_ID = int(os.getenv("CHAT_CHANNEL_ID"))

T1_ROLE_ID = int(os.getenv("T1_ROLE_ID"))
T4_ROLE_ID = int(os.getenv("T4_ROLE_ID"))
MANAGER_ROLE_ID = int(os.getenv("MANAGER_ROLE_ID"))
KOREAN_ROLE_ID = int(os.getenv("KOREAN_ROLE_ID"))
ENGLISH_ROLE_ID = int(os.getenv("ENGLISH_ROLE_ID"))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHAT_CHANNEL_ID)
    if channel:
        await channel.send("영이 봇 2.0ver 준비 완료! 뭐든 시켜줘")

# 역할 버튼
class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="T1~T3", style=discord.ButtonStyle.primary, custom_id="t1"))
        self.add_item(Button(label="T4", style=discord.ButtonStyle.success, custom_id="t4"))
        self.add_item(Button(label="Manager", style=discord.ButtonStyle.danger, custom_id="manager"))

@bot.command(name="역할")
async def role_cmd(ctx):
    await ctx.send("원하시는 역할을 선택해주세요:", view=RoleView())

@bot.command(name="class")
async def class_cmd(ctx):
    await role_cmd(ctx)

# 국가 버튼
class CountryView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Korean", style=discord.ButtonStyle.primary, custom_id="kr"))
        self.add_item(Button(label="English", style=discord.ButtonStyle.success, custom_id="en"))

@bot.command(name="국가")
async def country_cmd(ctx):
    await ctx.send("국가를 선택해주세요:", view=CountryView())

@bot.command(name="country")
async def country_alt_cmd(ctx):
    await country_cmd(ctx)

# 명령어 안내
@bot.command(name="명령어")
async def command_list(ctx):
    await ctx.send("사용 가능한 명령어: !역할 / !class / !국가 / !country / !명령어 / !command / !청소 / !영이 / !통계")

@bot.command(name="command")
async def command_alt(ctx):
    await command_list(ctx)

# 랜덤 메시지
import random
@bot.command(name="영이")
async def youngi(ctx):
    messages = ["안녕하세요~", "오늘도 화이팅!", "무엇을 도와드릴까요?", "영이는 귀여워요!", "명령을 기다리고 있어요!"]
    await ctx.send(random.choice(messages))

# 청소 기능
@bot.command(name="청소")
async def clean(ctx):
    roles = [T4_ROLE_ID, MANAGER_ROLE_ID]
    if any(role.id in roles for role in ctx.author.roles):
        deleted = await ctx.channel.purge(limit=5)
        await ctx.send(f"{len(deleted)}개의 메시지를 삭제했습니다.", delete_after=3)

# 통계 기능 (간단 예시)
@bot.command(name="통계")
async def stats(ctx):
    if any(role.id in [T4_ROLE_ID, MANAGER_ROLE_ID] for role in ctx.author.roles):
        await ctx.send("통계 기능은 준비 중입니다!")

# 버튼 클릭 핸들러
@bot.event
async def on_interaction(interaction):
    if interaction.data["component_type"] == 2:
        cid = interaction.data["custom_id"]
        member = interaction.user
        guild = member.guild

        if cid == "t1":
            role = guild.get_role(T1_ROLE_ID)
            await member.add_roles(role)
            await interaction.response.send_message("T1~T3 역할이 부여되었습니다!", ephemeral=True)

        elif cid == "t4":
            await member.add_roles(guild.get_role(T1_ROLE_ID))
            await guild.get_channel(ROLE_CHANNEL_ID).send(f"{member.mention} 님이 'T4' 역할을 신청했습니다.")
            await interaction.response.send_message("T1~T3 역할이 임시 부여되었습니다!", ephemeral=True)

        elif cid == "manager":
            await member.add_roles(guild.get_role(T1_ROLE_ID))
            await guild.get_channel(ROLE_CHANNEL_ID).send(f"{member.mention} 님이 'Manager' 역할을 신청했습니다.")
            await interaction.response.send_message("T1~T3 역할이 임시 부여되었습니다!", ephemeral=True)

        elif cid == "kr":
            await member.add_roles(guild.get_role(KOREAN_ROLE_ID))
            await interaction.response.send_message("Korean 역할이 부여되었습니다!", ephemeral=True)

        elif cid == "en":
            await member.add_roles(guild.get_role(ENGLISH_ROLE_ID))
            await interaction.response.send_message("English 역할이 부여되었습니다!", ephemeral=True)

# 새로운 유저 환영
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(
            f"""
{member.mention}님 환영합니다!!

환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!

1. A role exists on the server! Enter /!class/, /!country/ in the chat to create a choice After you select, you are granted access to the channel!
2. For mutual prevention of quarrels, please check the rules in the Notice-Rules to recognize simple rules and use them!
3. If you need additional server extensions or are limited in use, please contact your server administrator or executive if you need any services!
""")

keep_alive()
bot.run(TOKEN)
