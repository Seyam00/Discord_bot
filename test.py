import botT
import discord
import logging
import random
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
import asyncio

#await bot.reload_extension()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        members = [m for m in ctx.guild.members if not m.bot and m != ctx.author]
        slap = random.choice(members)
        return f"{ctx.author} slapped {slap} because *{argument}*"
    
@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    sa_reset_warning_as.start()
    #sa_reset_warning_eu.start()
    #sa_reset_warning_na.start()

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)

@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f"{member} joined on {member.joined_at}")

SERVER_OFFSET_HOURS = {
    "AS" : 8,
    "EU" : 1,
    "NA" : -5
}

sent_warning = False

def get_time_left_sa(server):
    server = server.upper()

    if server not in SERVER_OFFSET_HOURS:
        return None

    offset = SERVER_OFFSET_HOURS[server]
    
    now = datetime.now(timezone.utc) + timedelta(hours=offset)

    if now.day < 1 or (now.day == 1 and now.hour < 4):
        reset_date = now.replace(day=1, hour=4, minute=0, second=0)
    elif now.day < 16 or (now.day == 16 and now.hour < 4):
        reset_date = now.replace(day=16, hour=4, minute=0, second=0)
    else:
        next_month = now.month + 1 if now.month < 12 else 1
        next_year = now.year if now.month < 12 else now.year + 1
        reset_date = datetime(next_year, next_month, 1, 4, 0, 0)

    return reset_date - now

def get_time_left_it(server):
    server = server.upper()

    if server not in SERVER_OFFSET_HOURS:
        return None

    offset = SERVER_OFFSET_HOURS[server]
    
    now = datetime.now(timezone.utc) + timedelta(hours=offset)

    if now.day < 1 or (now.day == 1 and now.hour < 4):
        reset_date = now.replace(day=1, hour=4, minute=0, second=0)
    else:
        next_month = now.month + 1 if now.month < 12 else 1
        next_year = now.year if now.month < 12 else now.year + 1
        reset_date = datetime(next_year, next_month, 1, 4, 0, 0)

    return reset_date - now



@bot.command()
async def spiral_abyss(ctx, server: str):
    time_left = get_time_left_sa(server)
    if time_left is None:
        await ctx.send("Invalid Server! Use AS, EU or NA.")
        return
    await ctx.send(f"Time until next Spiral Abyss reset on {server} server: {time_left}")

@bot.command()
async def imaginarium_theatre(ctx, server: str):
    time_left = get_time_left_it(server)
    if time_left is None:
        await ctx.send("Invalid Server! Use AS, EU or NA.")
        return
    await ctx.send(f"Time until next Imaginarium Theatre reset on {server} server: {time_left}")

alert_sa = {"AS" : False, "EU" : False, "NA" : False}


@tasks.loop(minutes=5)
async def sa_reset_warning_as():
    
    for server in SERVER_OFFSET_HOURS:
        time_left = get_time_left_sa(server)

        if time_left is None:
            return
    
        if time_left < timedelta(hours=10) and not alert_sa[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Genshin Impact Spiral Abyss resets in n day!")
            alert_sa[server] = True
        if time_left > timedelta(days=4):
            alert_sa[server] = False



@tasks.loop(minutes=5)
async def it_reset_warning_as():
    global alert
    server = "AS"
    time_left = get_time_left_it(server)

    if time_left is None:
        return
    
    if time_left < timedelta(days=4) and not alert[server]:
        channel = discord.utils.get(bot.get_all_channels(), name="genshin-general")
        if channel:
            await channel.send(f"Genshin Impact Imaginarium Theatre resets in 1 day!")
        alert[server] = True
    if time_left > timedelta(days=4):
        alert[server] = False




handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

bot.run(botT.DISCORD_TOKEN, log_handler=None)

