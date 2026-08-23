import io
import json

import aiofiles
import aiohttp
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

from admin_utils import is_admin


# potentially add user to levels.json
async def level_add(user_id: str):
    async with aiofiles.open("levels.json", "r") as f:
        content = await f.read()
        data = json.loads(content)
    if user_id in data:
        return
    else:
        data[user_id] = [0, 1]
    async with aiofiles.open("levels.json", "w") as f:
        await f.write(json.dumps(data))


# update xp and level of user
async def add_xp(user_id: str, xp: int):
    async with aiofiles.open("levels.json", "r") as f:
        content = await f.read()
        data = json.loads(content)
    data[user_id][0] += xp
    data[user_id][1] += data[user_id][0] // 100
    data[user_id][0] = data[user_id][0] % 100
    async with aiofiles.open("levels.json", "w") as f:
        await f.write(json.dumps(data))


class LEVELCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # simple prototype
    @commands.command()
    async def mystats(self, ctx):
        async with aiofiles.open("levels.json", "r") as f:
            content = await f.read()
            data = json.loads(content)
        cur_xp = data[str(ctx.author.id)][0]
        cur_level = data[str(ctx.author.id)][1]
        person = ctx.author.display_name
        embed = discord.Embed(title=f"📊 {person}'s statistics")
        embed.description = f"""Your level: {cur_level}

        You need {100 - cur_xp} XP to get to the next level."""

        await ctx.send(embed=embed)

    @commands.command()
    async def quadratic(self, ctx):
        await ctx.send("This command is only a prototype for now. Lol.")

    @commands.command()
    @commands.check(is_admin)
    async def give_xp(self, ctx, user_id: str, amount: int):
        await level_add(user_id)
        await add_xp(user_id, amount)
        await ctx.send(f"I successfully gave {amount} XP to that user.")

    @commands.command()
    async def rank(self, ctx):
        await level_add(str(ctx.author.id))
        async with aiofiles.open("levels.json", "r") as f:
            content = await f.read()
            data = json.loads(content)
        cur_xp = f"{data[str(ctx.author.id)][0]} XP"
        cur_level = f"Level {data[str(ctx.author.id)][1]}"
        async with (
            aiohttp.ClientSession() as session,
            session.get(str(ctx.author.display_avatar.url)) as resp,
        ):
            avatar_bytes = await resp.read()

        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar = avatar.resize((128, 128))

        # turning the avatar into a circle (and pasting it to the card)
        card = Image.new("RGBA", (500, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)
        draw.rounded_rectangle([0, 0, 128, 128], radius=30, fill=(240, 100, 90))

        mask = Image.new("L", (128, 128), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, 128, 128], fill=255)

        card.paste(avatar, (30, 36), mask)

        draw.rounded_rectangle([170, 20, 480, 60], radius=20, fill=(240, 100, 90))
        draw.rounded_rectangle([170, 75, 480, 175], radius=20, fill=(240, 100, 90))

        font1 = ImageFont.truetype("Anta.ttf", 14)
        font2 = ImageFont.truetype("SpaceGrotesk.ttf", 14)
        # name
        draw.text(
            (185, 40),
            f"{ctx.author.name.upper()}",
            fill=(214, 118, 203),
            font=font1,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )
        # xp and level
        draw.text((185, 90), f"{cur_xp} / 100 XP", fill=(0, 0, 0), font=font2)
        draw.text((450, 90), f"{cur_level}", fill=(0, 0, 0), font=font2)

        bar_x1, bar_y1 = 185, 130
        bar_x2, bar_y2 = 465, 145

        xp_value = data[str(ctx.author.id)][0]

        draw.rounded_rectangle(
            [bar_x1, bar_y1, bar_x2, bar_y2], radius=8, fill=(220, 220, 220)
        )

        fill_width = int((bar_x2 - bar_x1) * (xp_value / 100))
        draw.rounded_rectangle(
            [bar_x1, bar_y1, bar_x1 + fill_width, bar_y2], radius=8, fill=(29, 163, 121)
        )

        # saving the image to memory
        buffer = io.BytesIO()
        card.save(buffer, format="PNG")
        buffer.seek(0)

        await ctx.send(file=discord.File(buffer, filename="rank.png"))


async def setup(bot):
    await bot.add_cog(LEVELCOG(bot))
