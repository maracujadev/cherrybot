import json

import aiofiles


async def is_admin(ctx):
    async with aiofiles.open("admins.json", "r") as f:
        content = await f.read()
        data = json.loads(content)

    guild_id = str(ctx.guild.id)

    if guild_id not in data:
        return False

    admin_role_id = data[guild_id]

    for role in ctx.author.roles:
        if str(role.id) == admin_role_id:
            return True

    return False
