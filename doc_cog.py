from discord.ext import commands


class DOCCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup")
    async def setup(self, ctx):
        await ctx.send(""">>> # How to set up the cherry bot
## Setting up an admin role
- this can only be done by the server owner
- there can only be one role capable of cherrybot-privileges
- please make sure only trusted members have this role
- type `%admin_add @[some_role]`
- type `%adminrole` to see the current admin role""")

    @commands.command(name="")
    async def reaction_role_manual(self, ctx):
        await ctx.send(""">>> # How to set up reaction role""")


async def setup(bot):
    await bot.add_cog(DOCCOG(bot))
