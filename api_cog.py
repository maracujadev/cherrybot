import os

import aiohttp
from discord.ext import commands

catapi_key = os.getenv("CATAPI_KEY")


class APICOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cat")
    async def cat(self, ctx):
        headers = {"x-api-key": catapi_key}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:  # noqa: SIM117
                async with session.get(
                    "https://api.thecatapi.com/v1/images/search"
                ) as img_resp:
                    img_data = await img_resp.json()
                    image_url = img_data[0]["url"]

            await ctx.send(image_url)
        except Exception as e:  # noqa: BLE001
            await ctx.send("Cant fetch a cat right now. Try again later.")
            print(f"Debug error: {e}")


async def setup(bot):
    await bot.add_cog(APICOG(bot))
