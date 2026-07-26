import discord
from discord.ext import commands 
from dotenv import load_dotenv
import os
import asyncio


load_dotenv() #reading from .env
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True # for reading messages
intents.members = True

bot = commands.Bot(command_prefix="#", intents=intents, case_insensitive=True)

######################

### terminal

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

### events

WELCOME_CHANNEL = 1516017173439582229

@bot.event
async def member_join(member):
	channel = bot.get_channel(WELCOME_CHANNEL)
	await channel.send(f"Welcome, {member.mention}!")

### commands

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def square(ctx, *, number=0):
	await ctx.send(str(int(number)**2))
	

@bot.command(name="67")
async def sixtyseven(ctx):
	await ctx.send("https://tenor.com/pU4XiE6POTB.gif")

@bot.command()
async def name(ctx, *, username=None):
	if username is None:
		await ctx.send("No name written. Try `#name Anna`.")
		return
	await ctx.send(f"hi, {username.strip().lower().capitalize()}")
	if username.strip().lower() == "alex":
		await ctx.send("thats a nice name btw!")

@bot.command()
async def poker(ctx):
	await ctx.send("Poker? I barely know her!")

@bot.command()
async def remind(ctx, amount: int, unit: str, *, message="something!"):
	unit = unit.strip().lower()

	if unit.startswith("min"):
		seconds = amount * 60
	elif unit.startswith("hour"):
		seconds = amount * 3600
	elif unit.startswith("sec"):
		seconds = amount
	else:
		await ctx.send("That didnt work. Try using seconds, minutes or hours.")
		return

	await ctx.send(f"Will do that! See ya in {amount} {unit}!")
	await asyncio.sleep(seconds)
	await ctx.send(f"{ctx.author.mention}, reminder: {message}")
	

############

bot.run(TOKEN)
