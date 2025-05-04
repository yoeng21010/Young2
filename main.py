from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
from discord.ui import View, Button
import os

# Flask keep_alive
app = Flask('')
@app.route('/')
def home():
    return "I'm alive!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_CHANNEL_ID = int(os.getenv("ROLE_CHANNEL_ID"))

class RoleButton(Button):
    def __init__(self, label, role_name):
        style = discord.ButtonStyle.success if role_name == "English" else discord.ButtonStyle.primary
        super().__init__(label=label, style=style)
        self.role_name = role_name

    async def callback(self, interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.role_name)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.name} 역할이 부여되었습니다!", ephemeral=True)

class GroupRoleButton(Button):
    def __init__(self, label, role_name, notify=False):
        color = discord.ButtonStyle.secondary if role_name == "연맹원" else discord.ButtonStyle.danger
        super().__init__(label=label, style=color)
        self.role_name = role_name
        self.notify = notify

    async def callback(self, interaction):
        member = interaction.user
        guild = interaction.guild
        basic_role = discord.utils.get(guild.roles, name="연맹원")
        if basic_role:
            await member.add_roles(basic_role)

        if self.notify:
            channel = bot.get_channel(ROLE_CHANNEL_ID)
            if channel:
                await channel.send(f"{member.mention} 님이 '{self.role_name}' 역할을 신청했습니다.")
        await interaction.response.send_message(f"{self.role_name} 역할 신청 완료! 연맹원 역할이 우선 부여되었습니다.", ephemeral=True)

class RoleSelectView(View):
    def __init__(self):
        super().__init__()
        self.add_item(GroupRoleButton("연맹원", "연맹원"))
        self.add_item(GroupRoleButton("임원", "임원", notify=True))
        self.add_item(GroupRoleButton("관리자", "관리자", notify=True))

class NationSelectView(View):
    def __init__(self):
        super().__init__()
        self.add_item(RoleButton("Korean", "Korean"))
        self.add_item(RoleButton("English", "English"))

@bot.command()
async def 역할(ctx):
    await ctx.send("원하는 역할을 선택해주세요!", view=RoleSelectView())

@bot.command()
async def 국가(ctx):
    await ctx.send("국가를 선택해주세요!", view=NationSelectView())

@bot.command()
async def 명령어(ctx):
    msg = "`!역할`, `!국가`, `!명령어`"
    await ctx.send(f"사용 가능한 명령어는 다음과 같습니다:
{msg}")

@bot.event
async def on_member_join(member):
    if member.guild.id != GUILD_ID:
        return
    channel = discord.utils.get(member.guild.text_channels, name="👋🏼환영합니다👋🏼")
    if channel:
        welcome = (
            f"{member.mention}
"
            "환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

"
            "1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
"
            "2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
"
            "3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!"
        )
        await channel.send(welcome)

keep_alive()
bot.run(os.getenv("TOKEN"))
