import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from f1_features import (
    get_next_race,
    get_current_Driverstanding,
    get_full_seasonSchedule,
    get_DriverDetails,
    get_constructor_standings
)

# Load token from .env
load_dotenv()  # Loads from .env in same folder
TOKEN = "Toke here"

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

    Prints the bot's username in the console to confirm that it is online.
    """
    print(f"✅ Bot is online as {bot.user}")


# ===============================
# Debug command
# ===============================
@bot.command()
async def ping(ctx):
    """
    Responds with 'Pong!' to confirm the bot is responsive.

    Args:
        ctx (commands.Context): The context in which the command is invoked.

    Returns:
        str: "Pong!" message in the same channel.
    """
    await ctx.send("Pong!")


# ===============================
# Command: Next race
# ===============================
@bot.command()
async def nextrace(ctx):
    """
    Fetch and display information about the next upcoming Formula 1 race.

    This includes race name, location, and date. Data is pulled using the
    `get_next_race()` function from `f1_features.py`.

    Args:
        ctx (commands.Context): The context in which the command is invoked.

    Returns:
        discord.Embed: An embed containing details of the next race.
    """
    try:
        race_info = get_next_race()
        embed = discord.Embed(
            title="Upcoming Race 🚩🚩🚩",
            description=race_info,
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error: {e}")


# ===============================
# Command: Driver standings
# ===============================
@bot.command()
async def dstandings(ctx, year: str = None):
    """
    Fetch and display the current driver standings for a specified Formula 1 season.

    If no year is provided, the command defaults to the current season.

    Args:
        ctx (commands.Context): The context in which the command is invoked.
        year (str, optional): Year of the F1 season (e.g., "2025"). Defaults to current year.

    Returns:
        str: A formatted standings table in monospaced code block.
    """
    try:
        # Convert to int if provided, else pass None
        standings_year = int(year) if year else None

        standings_table = get_current_Driverstanding(standings_year)
        await ctx.send(f"```Driver Standings {year}:\n{standings_table}\n```")
    except ValueError:
        await ctx.send("Invalid year format. Please enter a valid number (e.g., 2023).")
    except Exception as e:
        await ctx.send(f"Error: {e}")


# ===============================
# Command: Full Schedule
# ===============================
@bot.command()
async def fullschedule(ctx):
    """
    Fetch and display the full Formula 1 race schedule for the current season.

    The schedule includes race names and locations. It is sent as a `.txt` file
    due to Discord's message length limitations.

    Args:
        ctx (commands.Context): The context in which the command is invoked.

    Returns:
        discord.File: A file attachment containing the full season schedule.
    """
    try:
        currentSchedule = get_full_seasonSchedule()

        # Save to a file
        with open("schedule.txt", "w", encoding="utf-8") as f:
            f.write(currentSchedule)

        # Send file
        await ctx.send(file=discord.File("schedule.txt"))

    except Exception as e:
        await ctx.send(f"Error: {e}")


# ===============================
# Command: Driver Details (Commented Out)
# ===============================
'''
@bot.command()
async def driver(ctx, driver: str):
    """
    Get detailed information about a specific driver using driver number or driver code.

    Args:
        ctx (commands.Context): The context in which the command is invoked.
        driver (str): The driver's number or three-letter code (e.g., "44" or "VER").

    Returns:
        str: Detailed driver information including name, nationality, and team.
    """
    try:
        Ddetail = get_DriverDetails(driver)
        await ctx.send(f"**Driver's Detail:**\n{Ddetail}")
    except Exception as e:
        await ctx.send(f"Error: {e}")
'''


# ===============================
# Command: Constructor Standings
# ===============================
@bot.command()
async def cstandings(ctx, year: str = None):
    """
    Fetch and display the current constructor standings for a specified Formula 1 season.

    If no year is provided, the command defaults to the current season.

    Args:
        ctx (commands.Context): The context in which the command is invoked.
        year (str, optional): Year of the F1 season (e.g., "2025"). Defaults to current year.

    Returns:
        str: A formatted standings table in monospaced code block.
    """
    try:
        standings_year = int(year) if year else "current"

        constructor_standing = get_constructor_standings(standings_year)
        await ctx.send(f"```Constructor Standings {standings_year}:\n{constructor_standing}\n```")
    except Exception as e:
        await ctx.send(f"Error: {e}")


# ===============================
# Run the bot
# ===============================
bot.run(TOKEN)
