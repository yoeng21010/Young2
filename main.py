import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ui import Button, View
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_CHANNEL_ID = int(os.getenv("ROLE_CHANNEL_ID"))

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

    async def callback(self, interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.label)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role.name} 역할이 부여되었습니다.", ephemeral=True)
            if self.label in ["임원", "관리자"]:
                channel = interaction.guild.get_channel(ROLE_CHANNEL_ID)
                if channel:
                    await channel.send(f"**{interaction.user.mention}** 님이 '{self.label}' 역할을 신청했습니다.")

class LanguageButton(Button):
    def __init__(self, lang):
        super().__init__(label=lang, style=discord.ButtonStyle.success)

    async def callback(self, interaction):
        await interaction.response.send_message(f"{self.label} 언어를 선택하셨습니다!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"{bot.user} 봇 로그인 완료")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome-only")
    if channel:
        await channel.send("""**환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!**

1. 권한이 있어야 사용이 가능합니다! 영이봇의 안내에 따라 언어권과 본인의 인게임 역할을 선택해주세요.
2. 상호간 다툼 방지를 위해 공지-규칙을 확인해주세요.
3. 서버 증설, 기능 문의는 관리자나 임원에게 알려주세요!
""")
        role_view = View()
        for role_name, style in ROLE_OPTIONS.items():
            role_view.add_item(RoleButton(role_name, style))
        await channel.send("**역할을 선택해주세요:**", view=role_view)

        lang_view = View()
        for lang in LANGUAGE_OPTIONS:
            lang_view.add_item(LanguageButton(lang))
        await channel.send("**언어를 선택해주세요:**", view=lang_view)

@bot.command(name="국가")
async def 국가(ctx):
    view = View()
    for lang in LANGUAGE_OPTIONS:
        view.add_item(LanguageButton(lang))
    await ctx.send("**국가 선택 버튼입니다:**", view=view)

@bot.command(name="명령어")
async def 명령어(ctx):
    await ctx.send("""**사용 가능한 명령어:**

`!권한` - 역할 버튼 출력  
`!국가` - 국가 버튼 출력  
`!명령어` - 명령어 설명 출력
""")

@bot.command(name="권한")
async def 권한(ctx):
    view = View()
    for role_name, style in ROLE_OPTIONS.items():
        view.add_item(RoleButton(role_name, style))
    await ctx.send("**역할 선택 버튼입니다:**", view=view)

keep_alive()
bot.run(TOKEN)
