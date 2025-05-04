import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def 역할(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="연맹원", style=discord.ButtonStyle.primary, custom_id="role_연맹원"))
    view.add_item(discord.ui.Button(label="임원", style=discord.ButtonStyle.secondary, custom_id="role_임원"))
    view.add_item(discord.ui.Button(label="관리자", style=discord.ButtonStyle.danger, custom_id="role_관리자"))
    await ctx.send("원하는 역할을 선택하세요!", view=view)

@bot.command()
async def 국가(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Korean", style=discord.ButtonStyle.success, custom_id="nation_Korean"))
    view.add_item(discord.ui.Button(label="English", style=discord.ButtonStyle.secondary, custom_id="nation_English"))
    await ctx.send("국가를 선택하세요!", view=view)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="👋🏼환영합니다👋🏼")
    if channel:
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="역할 선택", style=discord.ButtonStyle.primary, custom_id="role_view"))
        view.add_item(discord.ui.Button(label="국가 선택", style=discord.ButtonStyle.success, custom_id="nation_view"))
        msg = """환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!

1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!
2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!
3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!
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

    if interaction.data["custom_id"] in role_map:
        role_name = role_map[interaction.data["custom_id"]]
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role:
            await interaction.user.add_roles(role)

        if interaction.data["custom_id"] in requested_role_map:
            request_channel = discord.utils.get(interaction.guild.text_channels, name="📌역할신청방📌")
            if request_channel:
                await request_channel.send(f"{interaction.user.mention} 님이 '{requested_role_map[interaction.data['custom_id']]}' 역할을 신청했습니다.")

        await interaction.response.send_message(f"{role_name} 역할이 부여되었습니다!", ephemeral=True)

    elif interaction.data["custom_id"] == "role_view":
        await 역할(await bot.get_context(interaction.message))
    elif interaction.data["custom_id"] == "nation_view":
        await 국가(await bot.get_context(interaction.message))

keep_alive()
bot.run(os.getenv("TOKEN"))