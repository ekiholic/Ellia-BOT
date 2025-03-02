# bot.py
import discord
from discord.ext import commands
from config import TOKEN
from commands.summon import summon_monster
from commands.inventory import show_inventory

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def summon(ctx):
    await summon_monster(ctx)

@bot.command()
async def inventory(ctx):
    await show_inventory(ctx)

bot.run(TOKEN)