
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected.")

@bot.command(name="역할")
async def role(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="T1~T3", style=discord.ButtonStyle.primary, custom_id="role_연맹원"))
    view.add_item(discord.ui.Button(label="T4", style=discord.ButtonStyle.secondary, custom_id="role_임원"))
    view.add_item(discord.ui.Button(label="Manager", style=discord.ButtonStyle.success, custom_id="role_관리자"))
    await ctx.send("역할을 선택하세요!", view=view)

@bot.command(name="class")
async def class_cmd(ctx):
    await role(ctx)

@bot.command(name="국가")
async def nation(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="한국어", style=discord.ButtonStyle.primary, custom_id="nation_Korean"))
    view.add_item(discord.ui.Button(label="English", style=discord.ButtonStyle.secondary, custom_id="nation_English"))
    await ctx.send("국가를 선택하세요!", view=view)

@bot.command(name="country")
async def country_cmd(ctx):
    await nation(ctx)

@bot.command(name="명령어")
async def commands_list(ctx):
    msg = "**[사용 가능한 명령어 목록]**\n"
    msg += "`!역할`, `!class`, `!국가`, `!country`, `!명령어`, `!command`"
    await ctx.send(msg)

@bot.command(name="command")
async def commands_alias(ctx):
    await commands_list(ctx)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="👋🏼환영합니다👋🏼")
    if channel:
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="역할 선택", style=discord.ButtonStyle.primary, custom_id="role_view"))
        view.add_item(discord.ui.Button(label="국가 선택", style=discord.ButtonStyle.success, custom_id="nation_view"))
        msg = (
            "환영합니다!! 간단한 서버에관한 소개를 도와드릴게요!\n"
            "1. 서버에 역할이 존재합니다! /!역할/, /!국가/ 을 채팅에 입력하면 선택지가 생성됩니다 선택후 채널입장권한이 부여됩니다!\n"
            "2. 상호간에 다툼방지를 위해서 간단한 규칙을 인지하기위해 공지-규칙에서 규칙을 확인후 이용바랍니다!\n"
            "3. 추가적인 서버증설이 필요하거나 이용이 제한됨, 필요한 서비스가있을시 서버관리자 혹은 임원에게 문의해주세요!\n\n"
            "1. A role exists on the server! Enter /!Role/, /!Country/ in the chat to create a choice After you select, you are granted access to the channel!\n"
            "2. For mutual prevention of quarrels, please check the rules in the Notice-Rules to recognize simple rules and use them!\n"
            "3. If you need additional server extensions or are limited in use, please contact your server administrator or executive if you need any services!"
        )
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
        await interaction.response.send_message(f"{role_name} 역할이 부여되었습니다!", ephemeral=True)

    if requested_role:
        channel = discord.utils.get(guild.text_channels, name="📌역할신청방📌")
        if channel:
            await channel.send(f"{interaction.user.name} 님이 **{requested_role}** 역할을 신청했습니다.")

keep_alive()
bot.run("YOUR_DISCORD_BOT_TOKEN")
