import aiohttp
import discord
from discord.ext import commands


class BirdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bird(self, ctx):
        async with (
            aiohttp.ClientSession() as session,
            session.get("https://api.some-random-api.com/animal/bird") as response,
        ):
            data = await response.json()

        await ctx.send(data["image"])
        await ctx.send(data["fact"])


async def setup(bot):
    await bot.add_cog(BirdCog(bot))
