
import discord
from discord.ext import commands
from discord.ui import View, Button
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_CHANNEL_ID = int(os.getenv("ROLE_CHANNEL_ID"))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    channel = bot.get_channel(ROLE_CHANNEL_ID)
    if channel:
        await send_welcome_message(channel)

async def send_welcome_message(channel):
    embed = discord.Embed(
        title="👋🏼환영합니다👋🏼",
        description=(
            "환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

"
            "1. 서버에 역할이 존재합니다! `/!역할/`, `/!국가/` 를 채팅에 입력하면 선택지가 생성됩니다 선택 후 채널 입장 권한이 부여됩니다!
"
            "2. 상호간에 다툼 방지를 위해서 간단한 규칙을 인지하기 위해 공지-규칙에서 규칙을 확인 후 이용 바랍니다!
"
            "3. 추가적인 서버 증설이 필요하거나 이용이 제한됨, 필요한 서비스가 있을 시 서버 관리자 혹은 임원에게 문의해주세요!"
        ),
        color=0x00ffcc
    )
    await channel.send(embed=embed)
    await channel.send(view=RoleView())
    await channel.send(view=NationView())

class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RoleButton("연맹원 (Member)", "연맹원", discord.ButtonStyle.success))
        self.add_item(RoleButton("임원 신청 (Executive Apply)", "임원", discord.ButtonStyle.primary))
        self.add_item(RoleButton("관리자 신청 (Admin Apply)", "관리자", discord.ButtonStyle.danger))

class RoleButton(Button):
    def __init__(self, label, role_name, style):
        super().__init__(label=label, style=style)
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        alliance_role = discord.utils.get(guild.roles, name="연맹원")
        target_role = discord.utils.get(guild.roles, name=self.role_name)
        await member.add_roles(alliance_role)
        if self.role_name in ["임원", "관리자"]:
            channel = discord.utils.get(guild.text_channels, id=ROLE_CHANNEL_ID)
            if channel:
                await channel.send(f"@here, 사용자 **{member.display_name}**님이 '{self.role_name}' 역할을 신청했습니다.")
        await interaction.response.send_message(f"'{self.label}' 선택 완료! (역할: 연맹원 부여됨)", ephemeral=True)

class NationView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(NationButton("대한민국 (Korean)", "Korean", discord.ButtonStyle.success))
        self.add_item(NationButton("영어권 (English)", "English", discord.ButtonStyle.primary))

class NationButton(Button):
    def __init__(self, label, role_name, style):
        super().__init__(label=label, style=style)
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=self.role_name)
        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"국가 역할 '{self.label}' 이 부여되었습니다!", ephemeral=True)

@bot.command()
async def 역할(ctx):
    await ctx.send(view=RoleView())

@bot.command()
async def 국가(ctx):
    await ctx.send(view=NationView())

@bot.command()
async def 명령어(ctx):
    await ctx.send("사용 가능한 명령어:
- !역할 : 역할 선택 버튼 표시
- !국가 : 국가 선택 버튼 표시
- !명령어 : 이 도움말 표시")

keep_alive()
bot.run(os.getenv("TOKEN"))
