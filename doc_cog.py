from discord.ext import commands


class DOCCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="docs")
    async def documentation(self, ctx):
        await ctx.send("")

    @commands.command(name="setup")
    async def setup(self, ctx):
        await ctx.send(""">>> # How to set up the cherry bot
## Setting up an admin role
- this can only be done by the server owner
- there can only be one role capable of cherrybot-privileges
- please make sure only trusted members have this role
- type `%admin_add @[some_role]`
- type `%adminrole` to see the current admin role

## Setting up a welcome channel
- this assigns a specific channel from your server where a welcome message will be sent
- this can only be done by someone with the local cherrybot admin role
- use `%welcome_add [mention-channel]` to set a new channel or replacing the old one
- use `%welcome_remove` to remove the local channel assignment
- use `%welcome_see` to see your local channel assignment""")

    @commands.command(name="reaction_setup")
    async def reaction_role_manual(self, ctx):
        await ctx.send(""">>> # How to set up reaction roles""")


async def setup(bot):
    await bot.add_cog(DOCCOG(bot))
