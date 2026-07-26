import discord
from discord.ext import commands 
from dotenv import load_dotenv
import os


load_dotenv() #reading from .env
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True # for reading messages

bot = commands.Bot(command_prefix="#", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def square(ctx, *, number=0):
	await ctx.send(str(int(number)**2))
	

@bot.command(name="67")
async def sixtyseven(ctx):
	await ctx.send("67?")

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
	
bot.run(TOKEN)
