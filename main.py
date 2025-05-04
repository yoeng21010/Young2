
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def 국가(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="한국", style=discord.ButtonStyle.primary, custom_id="nation_Korean"))
    view.add_item(discord.ui.Button(label="English", style=discord.ButtonStyle.secondary, custom_id="nation_English"))
    await ctx.send("국가를 선택하세요!", view=view)

@bot.command()
async def 역할(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="T1~T3", style=discord.ButtonStyle.primary, custom_id="role_연맹원"))
    view.add_item(discord.ui.Button(label="T4", style=discord.ButtonStyle.secondary, custom_id="role_임원"))
    view.add_item(discord.ui.Button(label="Manager", style=discord.ButtonStyle.success, custom_id="role_관리자"))
    await ctx.send("역할을 선택하세요!", view=view)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="👋🏼환영합니다👋🏼")
    if channel:
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="역할 선택", style=discord.ButtonStyle.primary, custom_id="role_view"))
        view.add_item(discord.ui.Button(label="국가 선택", style=discord.ButtonStyle.success, custom_id="nation_view"))
        msg = """
환영합니다!! 간단한 서버에 관한 소개를 도와드릴게요!

1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택 후 채널 입장 권한이 부여됩니다!
2. 상호간에 다툼 방지를 위해서 간단한 규칙을 인지하기 위해 공지-규칙에서 규칙을 확인 후 이용 바랍니다!
3. 추가적인 서버 증설이 필요하거나 이용이 제한됨, 필요한 서비스가 있을 시 서버 관리자 혹은 임원에게 문의해주세요!

---

Welcome!! Let me briefly introduce this server!

1. A role exists on the server! Enter /!Role/, /!Country/ in the chat to create a choice. After you select, you are granted access to the channel!
2. For mutual prevention of quarrels, please check the rules in the Notice-Rules to recognize simple rules and use them!
3. If you need additional server extensions or are limited in use, please contact your server administrator or executive if you need any services!
"""
        await channel.send(msg, view=view)

@bot.event
async def on_interaction(interaction):
    role_map = {
        "role_연맹원": "연맹원",
        "role_임원": "연맹원",
        "role_관리자": "연맹원",
        "nation_Korean": "Korean",
        "nation_English": "English"
    }
    requested_role_map = {
        "role_임원": "임원",
        "role_관리자": "관리자"
    }

    guild = interaction.guild
    role_name = role_map.get(interaction.data["custom_id"])
    requested_role = requested_role_map.get(interaction.data["custom_id"])
    role = discord.utils.get(guild.roles, name=role_name)

    if role:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"{role.name} 역할이 부여되었습니다!", ephemeral=True)

    if requested_role:
        channel = discord.utils.get(guild.text_channels, name="📌역할신청방📌")
        if channel:
            await channel.send(f"{interaction.user.mention} 님이 {requested_role} 역할을 신청했습니다.")

bot.run("YOUR_DISCORD_BOT_TOKEN")
