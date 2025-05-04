import discord
from discord.ext import commands
from discord.ui import Button, View
from keep_alive import keep_alive

TOKEN = "여기에_디스코드_토큰"
GUILD_ID = 123456789012345678
WELCOME_CHANNEL_ID = 123456789012345678  # 👋🏼환영합니다👋🏼 채널
NOTIFY_CHANNEL_ID = 123456789012345678   # 📌역할신청방📌 채널

ROLE_OPTIONS = {
    "연맹원": discord.ButtonStyle.secondary,
    "임원": discord.ButtonStyle.primary,
    "관리자": discord.ButtonStyle.danger,
}

LANGUAGE_OPTIONS = ["Korean", "English"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class RoleButton(Button):
    def __init__(self, role_name, style):
        super().__init__(label=role_name, style=style)
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=self.role_name if self.role_name == "연맹원" else "연맹원")
        if role:
            await interaction.user.add_roles(role)
            if self.role_name in ["임원", "관리자"]:
                notify_channel = bot.get_channel(NOTIFY_CHANNEL_ID)
                if notify_channel:
                    await notify_channel.send(f"{interaction.user.mention} 님이 '{self.role_name}' 역할을 신청했습니다.")
            await interaction.response.send_message(f"'{self.role_name}' 역할이 부여되었습니다!", ephemeral=True)
        else:
            await interaction.response.send_message("해당 역할을 찾을 수 없습니다.", ephemeral=True)

class LanguageButton(Button):
    def __init__(self, language):
        super().__init__(label=language, style=discord.ButtonStyle.success)
        self.language = language

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.language)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{self.language} 역할이 부여되었습니다!", ephemeral=True)
        else:
            await interaction.response.send_message("해당 역할이 존재하지 않습니다.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"{bot.user} is now running.")
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel:
        embed = discord.Embed(
            title="환영합니다!",
            description=(
                "환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

"
                "1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
"
                "2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
"
                "3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!"
            ),
            color=discord.Color.blue()
        )
        await welcome_channel.send(embed=embed)

@bot.command()
async def 역할(ctx):
    view = View()
    for name, style in ROLE_OPTIONS.items():
        view.add_item(RoleButton(name, style))
    await ctx.send("역할을 선택해주세요!", view=view)

@bot.command()
async def 국가(ctx):
    view = View()
    for language in LANGUAGE_OPTIONS:
        view.add_item(LanguageButton(language))
    await ctx.send("언어를 선택해주세요!", view=view)

keep_alive()
bot.run(TOKEN)
