import discord
from discord.ext import commands
from discord.ui import Button, View
from keep_alive import keep_alive
import os

TOKEN = os.environ['TOKEN']
OWNER_ID = int(os.environ['OWNER_ID'])
GUILD_ID = int(os.environ['GUILD_ID'])
ROLE_CHANNEL_ID = int(os.environ['ROLE_CHANNEL_ID'])

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
        role = discord.utils.get(interaction.guild.roles, name=self.role_name)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{self.role_name} 역할이 부여되었습니다.", ephemeral=True)
        else:
            await interaction.response.send_message("해당 역할을 찾을 수 없습니다.", ephemeral=True)

class LanguageButton(Button):
    def __init__(self, language):
        super().__init__(label=language, style=discord.ButtonStyle.success)
        self.language = language

    async def callback(self, interaction):
        await interaction.response.send_message(f"{self.language} 언어를 선택하셨습니다!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"{bot.user} 봇 로그인 완료")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome-only")
    if channel:
        await channel.send(
            "**사용 가능한 명령어:**
"
            "`!권한` - 역할 버튼 출력
"
            "`!국가` - 국가 버튼 출력
"
            "`!명령어` - 명령어 설명 출력"
        )
        role_view = View()
        for role_name, style in ROLE_OPTIONS.items():
            role_view.add_item(RoleButton(role_name, style))
        await channel.send("역할을 선택해주세요:", view=role_view)

@bot.command(name="국가")
async def 국가(ctx):
    view = View()
    for lang in LANGUAGE_OPTIONS:
        view.add_item(LanguageButton(lang))
    await ctx.send("언어 선택 버튼:", view=view)

@bot.command(name="권한")
async def 권한(ctx):
    view = View()
    for role_name, style in ROLE_OPTIONS.items():
        view.add_item(RoleButton(role_name, style))
    await ctx.send("역할 버튼:", view=view)

@bot.command(name="명령어")
async def 명령어(ctx):
    await ctx.send(
        "**사용 가능한 명령어:**
"
        "`!권한` - 역할 버튼 출력
"
        "`!국가` - 국가 버튼 출력
"
        "`!명령어` - 명령어 설명 출력"
    )

keep_alive()
bot.run(TOKEN)