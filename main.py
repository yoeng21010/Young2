
import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def 국가(ctx):
    view = View()
    view.add_item(Button(label="Korean", style=discord.ButtonStyle.primary, custom_id="korean"))
    view.add_item(Button(label="English", style=discord.ButtonStyle.success, custom_id="english"))
    await ctx.send("국가를 선택해주세요:", view=view)

@bot.command()
async def 역할(ctx):
    view = View()
    view.add_item(Button(label="연맹원", style=discord.ButtonStyle.secondary, custom_id="member"))
    view.add_item(Button(label="임원", style=discord.ButtonStyle.danger, custom_id="officer"))
    view.add_item(Button(label="관리자", style=discord.ButtonStyle.primary, custom_id="admin"))
    await ctx.send("역할을 선택해주세요:", view=view)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="👋🏼환영합니다👋🏼")
    if channel:
        msg = (
            f"환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

"
            f"1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
"
            f"2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
"
            f"3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!"
        )
        await channel.send(msg)

@bot.event
async def on_interaction(interaction):
    role_name = None
    if interaction.data["custom_id"] == "korean":
        role_name = "Korean"
    elif interaction.data["custom_id"] == "english":
        role_name = "English"
    elif interaction.data["custom_id"] == "member":
        role_name = "연맹원"
    elif interaction.data["custom_id"] in ["officer", "admin"]:
        role_name = "연맹원"
        apply_channel = discord.utils.get(interaction.guild.text_channels, name="📌역할신청방📌")
        if apply_channel:
            await apply_channel.send(f"{interaction.user.mention}님이 '{interaction.data['custom_id']}' 역할을 신청했습니다.")

    if role_name:
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"{role_name} 역할이 부여되었습니다!", ephemeral=True)
        else:
            await interaction.response.send_message("역할이 서버에 존재하지 않습니다.", ephemeral=True)

bot.run(os.getenv("TOKEN"))
