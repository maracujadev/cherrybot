import asyncio
import json
import os
from datetime import datetime, timezone

import aiofiles
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # reading from .env
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # for reading messages
intents.members = True

bot = commands.Bot(command_prefix="#", intents=intents, case_insensitive=True)

##### UNIVERSAL CONSTANTS

start_time = datetime.now(timezone.utc)

##### TERMINAL


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} at {start_time}")
    print(f"Tracking {len(bot.guilds)} servers with {len(bot.users)} users.")
    activity = discord.Activity(
        type=discord.ActivityType.listening, name="to the trees"
    )
    await bot.change_presence(activity=activity)


##############################################################


@bot.command()
async def docs(ctx):
    await ctx.send(""">>>The cherrybot has the following features:
------------------------------------------
`#ping`
-->replies 'pong!'; test for uptime
`#uptime`
-->replies uptime length
`#67`
-->let it surprise you
`#remind [amount] [unit]`
-->will send a reminder in the given time
`#avatar [user]`
-->sends the given user's avatar or your own if none is given
`#todo add [task]`
-->adds [task] to your todo-list
`#todo remove [index]`
-->removes the given task number
`#todo see`
-->responds with your to do list elements
`#bird`
-->responds with a random bird image and fact (unrelated)
`#createrole [hex] [role-name]`
-->creates a new role with color and name""")


##### ADMIN TOOLS


def is_admin(ctx):
    with open("admins.json", "r") as f:
        data = json.load(f)

    guild_id = str(ctx.guild.id)

    if guild_id not in data:
        return False

    admin_role_id = data[guild_id]

    for role in ctx.author.roles:
        if str(role.id) == admin_role_id:
            return True

    return False


@bot.command()
async def admin_add(ctx, role: discord.Role):
    if ctx.author.id != ctx.guild.owner_id:
        await ctx.send("Only the owner can use this command.")
        return
    async with aiofiles.open("admins.json", "r") as f:
        content = await f.read()
        data = json.loads(content)

    guild_id = str(ctx.guild.id)

    data[guild_id] = str(role.id)

    async with aiofiles.open("admins.json", "w") as f:
        await f.write(json.dumps(data))

    await ctx.send("Done! Added an admin role for the server.")


##### BASIC COMMANDS


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! My latency is {round(bot.latency * 1000, 2)}ms.")


@bot.command()
async def uptime(ctx):
    delta = datetime.now(timezone.utc) - start_time
    await ctx.send(f"This instance has been running for {delta}.")


@bot.command()
async def stats(ctx):
    await ctx.send(
        f"I am currently held hostage in {len(bot.guilds)} servers, helping out {len(bot.users)} users."
    )


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
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member is None:
        await ctx.send("Couldnt find anyone.")
        return

    await ctx.send(member.display_avatar.url)


@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Could not find that person.")
    else:
        raise error


##### TO DO SYSTEM


@bot.group(invoke_without_command=True)
async def todo(ctx):
    await ctx.send(
        ">>> Use #`todo add ...` to add a task \n"
        "Use #`todo remove (index)` to remove a task \n"
        "Use #`todo see` to see all your tasks"
    )


@todo.command(name="add")
async def todo_add(ctx, *, task: str):
    async with aiofiles.open("todo.json", "r") as f:
        content = await f.read()
        data = json.loads(content)

    user_id = str(ctx.author.id)

    if user_id not in data:
        data[user_id] = []

    data[user_id].append(task)

    async with aiofiles.open("todo.json", "w") as f:
        await f.write(json.dumps(data))

    await ctx.send("Added your new task!")


@todo.command(name="remove")
async def todo_remove(ctx, index: int):

    async with aiofiles.open("todo.json", "r") as f:
        content = await f.read()
        data = json.loads(content)
    user_id = str(ctx.author.id)

    if user_id not in data or not data[user_id]:
        await ctx.send("You don't have any tasks yet!")
        return

    if index - 1 >= len(data[user_id]) or index <= 0:
        await ctx.send("Not a valid index! Try again.")
        return

    data[user_id].remove(data[user_id][index - 1])

    async with aiofiles.open("todo.json", "w") as f:
        await f.write(json.dumps(data))

    await ctx.send(f"Removed task {index}.")


@todo.command(name="see")
async def todo_see(ctx):
    async with aiofiles.open("todo.json", "r") as f:
        content = await f.read()
        data = json.loads(content)
    user_id = str(ctx.author.id)

    if user_id not in data or not data[user_id]:
        await ctx.send("You don't have any tasks yet!")
        return

    message = ""
    for i in range(len(data[user_id])):
        message += f"{i + 1}) {data[user_id][i]} \n"
    await ctx.send(message + "\nFeel free to add or remove tasks.")


##### API CALLING


##### REACTION ROLES


@bot.command()
@commands.check(is_admin)
async def createrole(ctx, hex_color: str, *, role_name: str):
    hex_color = hex_color[1:]
    try:
        role_color = int(hex_color, 16)
    except ValueError:
        await ctx.send("Thats not an accepted color. Try again.")
        return
    await ctx.guild.create_role(name=role_name, colour=discord.Colour(role_color))


@bot.command()
@commands.check(is_admin)
async def announce(ctx, *, text: str):
    await ctx.send(">>> " + text)


@bot.command()
@commands.check(is_admin)
async def addreact(ctx, msg_id: int, emoji: str, role: discord.Role):
    message = await ctx.channel.fetch_message(msg_id)
    msg_id = str(msg_id)
    await message.add_reaction(emoji)

    async with aiofiles.open("reaction_roles.json", "r") as f:
        content = await f.read()
        data = json.loads(content)

    if msg_id not in data:
        data[msg_id] = {}

    data[msg_id][emoji] = role.id

    async with aiofiles.open("reaction_roles.json", "w") as f:
        await f.write(json.dumps(data))


##### EVENTS


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    async with aiofiles.open("reaction_roles.json", "r") as f:
        content = await f.read()
        data = json.loads(content)

    msg_id = str(payload.message_id)

    if msg_id not in data:
        return
    emoji = str(payload.emoji)

    if emoji not in data[msg_id]:
        return

    role_id = data[msg_id][emoji]
    guild = bot.get_guild(payload.guild_id)
    role = guild.get_role(int(role_id))
    member = guild.get_member(payload.user_id)

    await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return

    async with aiofiles.open("reaction_roles.json", "r") as f:
        content = await f.read()
        data = json.loads(content)

    msg_id = str(payload.message_id)

    if msg_id not in data:
        return

    emoji = str(payload.emoji)

    if emoji not in data[msg_id]:
        return

    role_id = data[msg_id][emoji]
    guild = bot.get_guild(payload.guild_id)
    role = guild.get_role(int(role_id))
    member = guild.get_member(payload.user_id)

    await member.remove_roles(role)


WELCOME_CHANNEL = 1516017173439582229


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL)
    await channel.send(f"Welcome, {member.mention}!")


############


async def load_extensions():
    await bot.load_extension("bird_cog")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
