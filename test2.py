# part of main
#------------------------------------------------------------------------------------------------------------------
import botT 
import discord
import logging
import random
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned_or
from datetime import datetime, timedelta, timezone
import asyncio

#await bot.reload_extension()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=when_mentioned_or("_"), intents=intents)
#------------------------------------------------------------------------------------------------------------------

#I made these commands when I started working on it just to test stuff, they can be anywhere or removed at some point
#------------------------------------------------------------------------------------------------------------------
class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        members = [m for m in ctx.guild.members if not m.bot and m != ctx.author]
        slap = random.choice(members)
        return f"{ctx.author} slapped {slap} because *{argument}*"
    
@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)

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
#------------------------------------------------------------------------------------------------------------------

#this should probably be part of main since it starts the events
#------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    sa_reset_warning_as.start()
    it_reset_warning_as.start()
    print([c.name for c in bot.commands])
#------------------------------------------------------------------------------------------------------------------

#This is where I calculate the times left for both 2 functions, there will be at least 6 more of these in the future with some little changes
#------------------------------------------------------------------------------------------------------------------
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
        reset_date = datetime(next_year, next_month, 1, 4, 0, 0, tzinfo=now.tzinfo)

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
        reset_date = datetime(next_year, next_month, 1, 4, 0, 0, tzinfo=now.tzinfo)

    return reset_date - now
#------------------------------------------------------------------------------------------------------------------

# These 2 commands show how much time left on these 2 modes when called for, somewhat small and simple so I am guessign these can be in a single file?
#------------------------------------------------------------------------------------------------------------------
@bot.command(name="spiral_abyss", aliases=["sa", "abyss", "spiralabyss", "Sa", "SA", "Abyss", "Spiral_abyss", "spiral", "Spiral"])
async def spiral_abyss(ctx, server: str):
    time_left_sa = get_time_left_sa(server)
    if time_left_sa is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until next Spiral Abyss reset on {server} server: {time_left_sa}")

@bot.command(name="imaginarium_theater", aliases=["it", "theater", "It", "Theater", "Imaginarium_theater", "IT"])
async def it(ctx, server: str):
    time_left_it = get_time_left_it(server)
    if time_left_it is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until next Imaginarium Theater on {server} server: {time_left_it}")
#------------------------------------------------------------------------------------------------------------------

#this was for debugging, can be ignored for now
#------------------------------------------------------------------------------------------------------------------
@it.error
async def it_error(ctx, error):
    await ctx.send(f"Error: `{error}`\nUsage: `_it AS|EU|NA`  (example: `_it NA`)")

alert_sa = {"AS" : False, "EU" : False, "NA" : False}
#------------------------------------------------------------------------------------------------------------------

# These are the alert functions that triggers automatically when conditions are met, I am not sure if I should make seperate files for these or just one for all alerts
#------------------------------------------------------------------------------------------------------------------
@tasks.loop(minutes=5)
async def sa_reset_warning_as():
    
    for server in SERVER_OFFSET_HOURS:
        time_left_sa = get_time_left_sa(server)

        if time_left_sa is None:
            continue
    
        if time_left_sa < timedelta(days=1) and not alert_sa[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Genshin Impact Spiral Abyss resets in 1 day!")
            alert_sa[server] = True
        if time_left_sa > timedelta(days=4):
            alert_sa[server] = False


alert_it = {"AS" : False, "EU" : False, "NA" : False}

@tasks.loop(minutes=5)
async def it_reset_warning_as():

    for server in SERVER_OFFSET_HOURS:
        time_left_it = get_time_left_it(server)

        if time_left_it is None:
            continue

        if time_left_it < timedelta(days=1) and not alert_it[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Genshin Impact Imaginarium Theater resets in 1 day!")
            alert_it[server] = True
        if time_left_it > timedelta(days=4):
            alert_it[server] = False
#------------------------------------------------------------------------------------------------------------------

#part of logger
#------------------------------------------------------------------------------------------------------------------
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
#------------------------------------------------------------------------------------------------------------------

#This should be in main ig
bot.run(botT.DISCORD_TOKEN, log_handler=None)

###