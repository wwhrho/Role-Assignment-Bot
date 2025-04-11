import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1278677581209796618
AUTH_CHANNEL_ID = 1358474101672382696
ROLE_TO_ADD = "UNION CITIZEN"
ROLE_TO_REMOVE = "Undocumented"

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 완료")

@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id != AUTH_CHANNEL_ID:
        return

    name_match = re.search(r"이름\s*[:：]\s*(\S+)", message.content)
    family_match = re.search(r"가문\s*[:：]\s*(\S+)", message.content)

    if name_match and family_match:
        name = name_match.group(1)
        family = family_match.group(1)
        nickname = f"자유시민 {name} {family}"

        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(message.author.id)
        add_role = discord.utils.get(guild.roles, name=ROLE_TO_ADD)
        remove_role = discord.utils.get(guild.roles, name=ROLE_TO_REMOVE)

        if add_role:
            await member.add_roles(add_role)
        if remove_role:
            await member.remove_roles(remove_role)

        await member.edit(nick=nickname)
        await message.delete()

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
