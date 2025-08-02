import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from f1_features import get_next_race, get_current_Driverstanding, get_full_seasonSchedule,get_DriverDetails,get_constructor_standings

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up intents properly
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Debug command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")



# Command: Next race
@bot.command()
async def nextrace(ctx):
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


# Command: Driver standings
@bot.command()
async def dstandings(ctx, year: str = None):  # HIGHLIGHT: Made year optional
    try:
        # HIGHLIGHT: Convert to int if provided, else pass None
        standings_year = int(year) if year else None
        
        standings_table = get_current_Driverstanding(standings_year)
        await ctx.send(f"```Driver Standings {year}:\n{standings_table}\n```")
    except ValueError:
        await ctx.send("Invalid year format. Please enter a valid number (e.g., 2023).")
    except Exception as e:
        await ctx.send(f"Error: {e}")


# command: Full Schedule
@bot.command()
async def fullschedule(ctx):
    try:
        currentSchedule = get_full_seasonSchedule()
        
        # Save to a file
        with open("schedule.txt", "w", encoding="utf-8") as f:
            f.write(currentSchedule)
        
        # Send file
        await ctx.send(file=discord.File("schedule.txt"))

    except Exception as e:
        await ctx.send(f"Error: {e}")

#command: Driver Details
'''@bot.command()
async def driver(ctx, driver: str):
    """
    Get driver details using driver number or driver code.
    """
    try:
        Ddetail = get_DriverDetails(driver)
        await ctx.send(f"**Driver's Detail:**\n{Ddetail}")
    except Exception as e:
        await ctx.send(f"Error: {e}")
'''

#command: Constructor Standing
@bot.command()
async def cstandings(ctx, year: str = None):
    try:
        standings_year = int(year) if year else "current"
        
        constructor_standing = get_constructor_standings(standings_year)
        await ctx.send(f"```Constructor Standings {standings_year}:\n{constructor_standing}\n```")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
        

bot.run(TOKEN)


