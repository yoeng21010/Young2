
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import random
import os
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_IDS = {
    "T1~T3": 123456789012345678,
    "T4": 234567890123456789,
    "Manager": 345678901234567890
}
COUNTRY_ROLES = {
    "Korean": 456789012345678901,
    "English": 567890123456789012
}
WELCOME_CHANNEL_ID = 678901234567890123
CLASSCHANGE_CHANNEL_ID = 789012345678901234
CHAT_CHANNEL_ID = 890123456789012345

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHAT_CHANNEL_ID)
    if channel:
        await channel.send("영이 봇 2.0ver 준비 완료! 뭐든 시켜줘")

@bot.command()
async def 역할(ctx):
    await send_role_buttons(ctx)

@bot.command()
async def class_(ctx):
    await send_role_buttons(ctx)

async def send_role_buttons(ctx):
    view = View()
    for label, role in [("T1~T3", "T1~T3"), ("T4", "T4"), ("Manager", "Manager")]:
        async def callback(interaction, role=role):
            await interaction.user.add_roles(discord.Object(id=ROLE_IDS["T1~T3"]))
            if role != "T1~T3":
                class_channel = bot.get_channel(CLASSCHANGE_CHANNEL_ID)
                if class_channel:
                    await class_channel.send(f"**{interaction.user.display_name}** 님이 **{role}** 역할을 신청했습니다.")
            await interaction.response.send_message(f"{role} 역할 신청이 완료되었습니다!", ephemeral=True)
        btn = Button(label=role, style=discord.ButtonStyle.primary)
        btn.callback = callback
        view.add_item(btn)
    await ctx.send("원하는 역할을 선택해주세요!", view=view)

@bot.command()
async def 국가(ctx):
    await send_country_buttons(ctx)

@bot.command()
async def country(ctx):
    await send_country_buttons(ctx)

async def send_country_buttons(ctx):
    view = View()
    for label in COUNTRY_ROLES:
        async def callback(interaction, label=label):
            await interaction.user.add_roles(discord.Object(id=COUNTRY_ROLES[label]))
            await interaction.response.send_message(f"{label} 역할이 부여되었습니다!", ephemeral=True)
        btn = Button(label=label, style=discord.ButtonStyle.secondary)
        btn.callback = callback
        view.add_item(btn)
    await ctx.send("국가를 선택해주세요!", view=view)

@bot.command()
@commands.has_any_role("T4", "Manager")
async def 청소(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount}개의 메시지를 삭제했어요!", delete_after=3)

@bot.command()
@commands.has_any_role("T4", "Manager")
async def 영이(ctx):
    messages = [
        "오늘도 열심히!",
        "물 한 잔 마시고 가자!",
        "버튼 누르는 건 재밌지?",
        "나는 영이봇! 귀여움은 나의 힘!",
        "슬슬 과금할 시간이야~"
    ]
    await ctx.send(random.choice(messages))

@bot.command()
async def 명령어(ctx):
    await ctx.send("사용 가능한 명령어: !역할 (!class), !국가 (!country), !청소, !영이, !명령어 (!command)")

@bot.command()
async def command(ctx):
    await 명령어(ctx)

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel:
        message = (
            f"**{member.mention}님, 환영합니다!! 간단한 서버에 관한 소개를 도와드릴게요!**

"
            "**한국어**
"
            "1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택 후 채널 입장 권한이 부여됩니다!
"
            "2. 상호간에 다툼 방지를 위해서 간단한 규칙을 공지-규칙에서 확인 후 이용 바랍니다!
"
            "3. 추가적인 서버 증설이나 서비스 필요 시 서버 관리자나 임원에게 문의해주세요!

"
            "**English**
"
            "1. A role exists on the server! Type /!class/ or /!country/ to get started.
"
            "2. Please read the rules in the notice-rules channel before participating.
"
            "3. If you need more features, contact the server admin or executive!"
        )
        await welcome_channel.send(message)

keep_alive()
bot.run(os.environ["TOKEN"])
