#part of main
#------------------------------------------------------------------------------------------------------------------
#import botT 
import discord
import logging
import random
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned_or
from datetime import datetime, timedelta, timezone
import asyncio
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("No DISCORD_BOT_TOKEN found in environment!")



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

    for i in (
        sa_reset_warning_as, it_reset_warning_as, so_reset_warning_as,
        moc_reset_warning_as, pf_reset_warning_as, as_reset_warning_as,
        sd_reset_warning_as, da_reset_warning_as
    ):
        if not i.is_running():
            i.start()

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



def get_time_left_so(server):
    server = server.upper()
    if server not in SERVER_OFFSET_HOURS:
        return None

    tz = timezone(timedelta(hours=SERVER_OFFSET_HOURS[server]))

    now = datetime.now(tz)

    genshin_patch_day = datetime(year=2025, month=8, day=6, hour=4, minute=0, tzinfo=tz)
    next_patch_day    = datetime(year=2025, month=9, day=9, hour=4, minute=0, tzinfo=tz)

    remaining = next_patch_day - now
    return remaining if remaining.total_seconds() > 0 else timedelta(0)

def get_time_left_moc(server):
    server = server.upper()
    if server not in SERVER_OFFSET_HOURS:
        return None
    
    tz = timezone(timedelta(hours=SERVER_OFFSET_HOURS[server]))

    now = datetime.now(tz)

    anchor = datetime(year=2025, month=6, day=23, hour=4, minute=0, tzinfo=tz)
    cycle = timedelta(days=42)

    if now <= anchor:
        reset = anchor
    else:
        cycle_elapsed = (now - anchor) // cycle
        reset = anchor + (cycle_elapsed + 1) * cycle

    remaining = reset - now

    return remaining if remaining.total_seconds() > 0 else timedelta(0)

def get_time_left_pf(server):
    server = server.upper()
    if server not in SERVER_OFFSET_HOURS:
        return None
    
    tz = timezone(timedelta(hours=SERVER_OFFSET_HOURS[server]))

    now = datetime.now(tz)

    anchor = datetime(year=2025, month=7, day=21, hour=4, minute=0, tzinfo=tz)
    cycle = timedelta(days=42)

    if now <= anchor:
        reset = anchor
    else:
        cycle_elapsed = (now - anchor) // cycle
        reset = anchor + (cycle_elapsed + 1) * cycle

    remaining = reset - now

    return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
def get_time_left_as(server):
    server = server.upper()
    if server not in SERVER_OFFSET_HOURS:
        return None
    
    tz = timezone(timedelta(hours=SERVER_OFFSET_HOURS[server]))

    now = datetime.now(tz)

    anchor = datetime(year=2025, month=8, day=18, hour=4, minute=0, tzinfo=tz)
    cycle = timedelta(days=42)

    if now <= anchor:
        reset = anchor
    else:
        cycle_elapsed = (now - anchor) // cycle
        reset = anchor + (cycle_elapsed + 1) * cycle

    remaining = reset - now

    return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
def get_time_left_sd(server):
    server = server.upper()
    if server not in SERVER_OFFSET_HOURS:
        return None
    
    tz = timezone(timedelta(hours=SERVER_OFFSET_HOURS[server]))

    now = datetime.now(tz)

    anchor = datetime(year=2025, month=8, day=15, hour=4, minute=0, tzinfo=tz)
    cycle = timedelta(days=14)

    if now <= anchor:
        reset = anchor
    else:
        cycle_elapsed = (now - anchor) // cycle
        reset = anchor + (cycle_elapsed + 1) * cycle

    remaining = reset - now

    return remaining if remaining.total_seconds() > 0 else timedelta(0)

def get_time_left_da(server):
    server = server.upper()
    if server not in SERVER_OFFSET_HOURS:
        return None
    
    tz = timezone(timedelta(hours=SERVER_OFFSET_HOURS[server]))

    now = datetime.now(tz)

    anchor = datetime(year=2025, month=8, day=8, hour=4, minute=0, tzinfo=tz)
    cycle = timedelta(days=14)

    if now <= anchor:
        reset = anchor
    else:
        cycle_elapsed = (now - anchor) // cycle
        reset = anchor + (cycle_elapsed + 1) * cycle

    remaining = reset - now

    return remaining if remaining.total_seconds() > 0 else timedelta(0)
#------------------------------------------------------------------------------------------------------------------

#These 2 commands show how much time left on these 2 modes when called for, somewhat small and simple so I am guessign these can be in a single file?
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
    await ctx.send(f"Time until next Imaginarium Theater reset on {server} server: {time_left_it}")

@bot.command(name="stygian_onslaught", aliases=["stygian", "Stygian", "onslaught", "Onslaught", "so", "So", "SO", "sO"])
async def stygian_onslaught(ctx, server: str):
    time_left_so = get_time_left_so(server)
    if time_left_so is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until Stygian Onslaught ends on {server} server: {time_left_so}")

@bot.command(name="memory_of_chaos", aliases=["moc", "MOC", "Moc", "memory"])
async def memory_of_chaos(ctx, server: str):
    time_left_moc = get_time_left_moc(server)
    if time_left_moc is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until next Memory of Chaos reset on {server} server: {time_left_moc}")

@bot.command(name="pure_fiction", aliases=["PF", "Pf", "pf", "pure", "fiction"])
async def pure_fiction(ctx, server: str):
    time_left_pf = get_time_left_pf(server)
    if time_left_pf is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until next Pure Fiction reset on {server} server: {time_left_pf}")

@bot.command(name="apocalyptic_shadow", aliases=["AS", "As", "as", "apocalyptic", "Apocalyptic", "shadow", "Shadow"])
async def apocalyptic_shadow(ctx, server: str):
    time_left_as = get_time_left_as(server)
    if time_left_as is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until next Apocalyptic Shadow reset on {server} server: {time_left_as}")

@bot.command(name="shiyu_defense", aliases=["shiyu", "defense", "sd", "Sd", "SD", "sD", "Shiyu", "Defense"])
async def shiyu_defense(ctx, server: str):
    time_left_sd = get_time_left_sd(server)
    if time_left_sd is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until next Shiyu Defense reset on {server} server: {time_left_sd}")

@bot.command(name="deadly_assault", aliases=["da", "Da", "DA", "deadly", "Deadly", "assault", "Assault"])
async def deadly_assault(ctx, server: str):
    time_left_da = get_time_left_da(server)
    if time_left_da is None:
        await ctx.send("huh?")
        return
    await ctx.send(f"Time until next Deadly Assault reset on {server} server: {time_left_da}")
#------------------------------------------------------------------------------------------------------------------

#this was for debugging, can be ignored for now
#------------------------------------------------------------------------------------------------------------------
@it.error
async def it_error(ctx, error):
    await ctx.send(f"Error: `{error}`\nUsage: `_it AS|EU|NA`  (example: `_it NA`)")


#------------------------------------------------------------------------------------------------------------------

#These are the alert functions that triggers automatically when conditions are met, I am not sure if I should make seperate files for these or just one for all alerts
#------------------------------------------------------------------------------------------------------------------
alert_sa = {"AS" : False, "EU" : False, "NA" : False}

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

alert_so = {"AS" : False, "EU" : False, "NA" : False}

@tasks.loop(minutes=5)
async def so_reset_warning_as():

    for server in SERVER_OFFSET_HOURS:
        time_left_so = get_time_left_so(server)

        if time_left_so is None:
            continue

        if time_left_so < timedelta(days=1) and not alert_so[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Genshin Impact Stygian Onslaught resets in 1 day!")
            alert_so[server] = True
        if time_left_so > timedelta(days=4):
            alert_so[server] = False

alert_moc = {"AS" : False, "EU" : False, "NA" : False}

@tasks.loop(minutes=5)
async def moc_reset_warning_as():

    for server in SERVER_OFFSET_HOURS:
        time_left_moc = get_time_left_moc(server)

        if time_left_moc is None:
            continue

        if time_left_moc < timedelta(days=1) and not alert_moc[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Honkai Star Rail Memory of Chaos resets in 1 day!")
            alert_moc[server] = True
        if time_left_moc > timedelta(days=4):
            alert_moc[server] = False

alert_pf = {"AS" : False, "EU" : False, "NA" : False}

@tasks.loop(minutes=5)
async def pf_reset_warning_as():

    for server in SERVER_OFFSET_HOURS:
        time_left_pf = get_time_left_pf(server)

        if time_left_pf is None:
            continue

        if time_left_pf < timedelta(days=1) and not alert_pf[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Honkai Star Rail Pure Fiction resets in 1 day!")
            alert_pf[server] = True
        if time_left_pf > timedelta(days=4):
            alert_pf[server] = False

alert_as = {"AS" : False, "EU" : False, "NA" : False}

@tasks.loop(minutes=5)
async def as_reset_warning_as():

    for server in SERVER_OFFSET_HOURS:
        time_left_as = get_time_left_as(server)

        if time_left_as is None:
            continue

        if time_left_as < timedelta(days=1) and not alert_as[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Honkai Star Rail Apocalyptic Shadow resets in 1 day!")
            alert_as[server] = True
        if time_left_as > timedelta(days=4):
            alert_as[server] = False

alert_sd = {"AS" : False, "EU" : False, "NA" : False}

@tasks.loop(minutes=5)
async def sd_reset_warning_as():
    
    for server in SERVER_OFFSET_HOURS:
        time_left_sd = get_time_left_sd(server)

        if time_left_sd is None:
                continue
                
        if time_left_sd < timedelta(days=1) and not alert_sd[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Zenless Zone Zero Shiyu Defense resets in 1 day!")
            alert_sd[server] = True
        if time_left_sd > timedelta(days=4):
            alert_sd[server] = False

alert_da = {"AS" : False, "EU" : False, "NA" : False}

@tasks.loop(minutes=5)
async def da_reset_warning_as():

    for server in SERVER_OFFSET_HOURS:
        time_left_da = get_time_left_da(server)

        if time_left_da is None:
            continue

        if time_left_da < timedelta(days=1) and not alert_da[server]:
            channel = discord.utils.get(bot.get_all_channels(), name="experimental-fuckery")
            if channel:
                await channel.send(f"Zenless Zone Zero Deadly Assault resets in 1 day!")
            alert_da[server] = True
        if time_left_da > timedelta(days=4):
            alert_da[server] = False
#------------------------------------------------------------------------------------------------------------------

#part of logger
#------------------------------------------------------------------------------------------------------------------
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
#------------------------------------------------------------------------------------------------------------------

#This should be in main ig
bot.run(TOKEN, log_handler=None)

##
#Testing deployment protocol
#Testing deployment protocol2