import discord
from discord.ext import commands
from discord.ui import Button, View
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 123456789012345678
ROLE_CHANNEL_ID = 123456789012345678
WELCOME_CHANNEL_ID = 123456789012345678
NOTIFY_CHANNEL_ID = 123456789012345678

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_OPTIONS = {
    "연맹원": discord.ButtonStyle.secondary,
    "임원": discord.ButtonStyle.primary,
    "관리자": discord.ButtonStyle.danger
}

LANGUAGE_OPTIONS = ["English", "Korean"]

class RoleButton(Button):
    def __init__(self, role_name, style):
        super().__init__(label=role_name, style=style)
        self.role_name = role_name

    async def callback(self, interaction):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=self.role_name if self.role_name == "연맹원" else "연맹원")

        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"{role.name} 역할이 부여되었습니다!", ephemeral=True)

        if self.role_name in ["임원", "관리자"]:
            notify_channel = guild.get_channel(NOTIFY_CHANNEL_ID)
            if notify_channel:
                await notify_channel.send(f"📌 {member.mention} 님이 {self.role_name} 역할을 신청했습니다.")

class LanguageButton(Button):
    def __init__(self, language):
        super().__init__(label=language, style=discord.ButtonStyle.success)
        self.language = language

    async def callback(self, interaction):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=self.language)
        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"{self.language} 역할이 부여되었습니다!", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} 작동 시작!')

@bot.command()
async def 역할(ctx):
    view = View()
    for role, style in ROLE_OPTIONS.items():
        view.add_item(RoleButton(role, style))
    await ctx.send("원하는 역할을 선택해주세요!", view=view)

@bot.command()
async def 국가(ctx):
    view = View()
    for lang in LANGUAGE_OPTIONS:
        view.add_item(LanguageButton(lang))
    await ctx.send("국가를 선택해주세요!", view=view)

@bot.event
async def on_member_join(member):
    if member.guild.system_channel:
        view_roles = View()
        for role, style in ROLE_OPTIONS.items():
            view_roles.add_item(RoleButton(role, style))

        view_langs = View()
        for lang in LANGUAGE_OPTIONS:
            view_langs.add_item(LanguageButton(lang))

        welcome_msg = """환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!
"""
        await member.guild.system_channel.send(welcome_msg)
        await member.guild.system_channel.send("역할을 선택해주세요!", view=view_roles)
        await member.guild.system_channel.send("국가를 선택해주세요!", view=view_langs)

bot.run(TOKEN)
