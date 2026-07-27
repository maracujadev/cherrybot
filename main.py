import discord
from discord.ext import commands 
from dotenv import load_dotenv
import os
import asyncio
import json


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
async def docs(ctx):
	await ctx.send("The cherrybot has the following features:")
	await ctx.send("------------------------------------------")
	await ctx.send("`#ping`")
	await ctx.send("-->replies 'pong!'; test for uptime")
	await ctx.send("`#67`")
	await ctx.send("-->let it surprise you")
	await ctx.send("`#remind [amount] [unit]`")
	await ctx.send("-->will send a reminder in the given time")
	await ctx.send("`#avatar [user]")
	await ctx.send("-->sends the given user's avatar")
	await ctx.send("`#todo add [task]`")
	await ctx.send("-->adds [task] to your todo-list")
	await ctx.send("`#todo remove [index]`")
	await ctx.send("-->removes the given task number")
	await ctx.send("`#todo see`")
	await ctx.send("-->responds with your to do list elements")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

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
		if amount == 1:
			temp = "minute"
		else:
			temp = "minutes"
	elif unit.startswith("hour"):
		seconds = amount * 3600
		if amount == 1:
			temp = "hour"
		else:
			temp = "hours"
	elif unit.startswith("sec"):
		seconds = amount
		if amount == 1:
			temp = "second"
		else:
			temp = "seconds"
	else:
		await ctx.send("That didnt work. Try using seconds, minutes or hours.")
		return

	await ctx.send(f"Will do that! See ya in {amount} {temp}!")
	await asyncio.sleep(seconds)
	await ctx.send(f"{ctx.author.mention}, reminder: {message}")

@bot.command()
async def avatar(ctx, member: str = None):
	if member is None:
		found_member = ctx.author
	else:
		try:
			found_member = await commands.MemberConverter().convert(ctx, member)
		except:
			found_member = discord.utils.get(ctx.guild.members, name=member)

	if found_member is None:
		await ctx.send("Couldnt find anyone.")
		return

	await ctx.send(found_member.display_avatar.url)

### to do list commands

@bot.group(invoke_without_command=True)
async def todo(ctx):
	await ctx.send(
		"Use #`todo add ...` to add a task"
		"Use #`todo remove (index)` to remove a task"
		"Use #`todo see` to see all your tasks"
		)
@todo.command(name="add")
async def todo_add(ctx, *, task: str):
	with open("todo.json", "r") as f:
		data = json.load(f)

	user_id = str(ctx.author.id)

	if user_id not in data:
		data[user_id] = []

	data[user_id].append(task)

	with open("todo.json", "w") as f:
		json.dump(data, f)

	await ctx.send("Done!")

@todo.command(name="remove")
async def todo_remove(ctx, index: int):
	with open("todo.json", "r") as f:
		data = json.load(f)
	user_id = str(ctx.author.id)

	if user_id not in data or not data[user_id]:
		await ctx.send("You don't have any tasks yet!")
		return

	if index-1 >= len(data[user_id]) or index <= 0:
		await ctx.send("Not a valid index! Try again.")
		return

	data[user_id].remove(data[user_id][index-1])

	with open("todo.json", "w") as f:
		json.dump(data, f)

	await ctx.send("Done!")

@todo.command(name="see")
async def todo_see(ctx):
	with open("todo.json", "r") as f:
		data = json.load(f)
	user_id = str(ctx.author.id)

	if user_id not in data or not data[user_id]:
		await ctx.send("You don't have any tasks yet!")
		return

	for i in range(len(data[user_id])):
		await ctx.send(f"{i+1}) {data[user_id][i]}")
	await ctx.send("Feel free to add or remove tasks.")

############

bot.run(TOKEN)
