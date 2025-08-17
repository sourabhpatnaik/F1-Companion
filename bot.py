import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from f1_features import (
    get_next_race,
    get_current_Driverstanding,
    get_full_seasonSchedule,
    get_DriverDetails,
    get_constructor_standings,
    get_fullRacesession_Info,
    recentRaceResult
)

# Load token from .env
load_dotenv()  # Loads from .env in same folder
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up intents properly
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ===============================
# Event: Bot is ready
# ===============================
@bot.event
async def on_ready():
    """
    Triggered when the bot successfully logs in and is ready to use.
    """
    print(f"✅ Bot is online as {bot.user}")


# ===============================
# Debug command
# ===============================
@bot.command()
async def ping(ctx):
    """Responds with 'Pong!' 🏓"""
    await ctx.send("🏓 Pong!")


# ===============================
# Command: Next race
# ===============================
@bot.command()
async def nextrace(ctx):
    """📅 Shows info about the next upcoming Formula 1 race."""
    try:
        race_info = get_next_race()
        embed = discord.Embed(
            title="🏁 Upcoming Race 🚩",
            description=race_info,
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


# ===============================
# Command: Driver standings
# ===============================
@bot.command()
async def dstandings(ctx, year: str = None):
    """🏎️ Shows driver standings for the specified year."""
    try:
        standings_year = int(year) if year else None
        standings_table = get_current_Driverstanding(standings_year)
        await ctx.send(f"```🏆 Driver Standings {year or 'Current'}:\n{standings_table}\n```")
    except ValueError:
        await ctx.send("⚠️ Invalid year format. Please enter a valid number (e.g., 2023).")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


# ===============================
# Command: Full Schedule
# ===============================
@bot.command()
async def fullschedule(ctx):
    """🗓️ Shows the full race schedule for the current season."""
    try:
        currentSchedule = get_full_seasonSchedule()

        with open("schedule.txt", "w", encoding="utf-8") as f:
            f.write(currentSchedule)

        await ctx.send(file=discord.File("schedule.txt"))

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


# ===============================
# Command: Constructor Standings
# ===============================
@bot.command()
async def cstandings(ctx, year: str = None):
    """🏢 Shows constructor standings for the specified year."""
    try:
        standings_year = int(year) if year else "current"
        constructor_standing = get_constructor_standings(standings_year)
        await ctx.send(f"```🏆 Constructor Standings {standings_year}:\n{constructor_standing}\n```")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


# ===============================
# Command: Full Session Details
# ===============================
@bot.command()
async def fullsession(ctx, country: str, year: int):
    """📋 Shows all race session details for a given country and year."""
    try:
        table_str = get_fullRacesession_Info(country.title(), year)
        await ctx.send(f"```📋 Full Session Details:\n{table_str}```")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


# ===============================
# Command: Last Race Result
# ===============================
@bot.command()
async def lastraceresult(ctx):
    """🥇 Shows last race results."""
    try:
        race_detail = recentRaceResult()
        await ctx.send(f"```🏁 Last Race Results 🏆:\n{race_detail}```")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")





@bot.command(name="driver")
async def driver(ctx, season: str, driver_code_or_number: str):
    """
    Usage: !driver <season> <driver_code_or_number>
    Example: !driver 2023 VER
    """
    await ctx.send("Fetching driver details...")

    result = get_DriverDetails(driver_code_or_number, season)

    # Send formatted output
    await ctx.send(f"```{result}```")


# ===============================
# Run the bot
# ===============================
bot.run(TOKEN)
