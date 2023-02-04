import discord

from Database.Models.node import Node
from Database.Models.user import User


async def spawn_user(user: discord.User):
    await User.filter(discord_id=user.id).delete()

    await User.create(name="test", discord_id=user.id)


async def move_to(member: discord.Member, node: Node):

    # clear their roles
    for role in member.roles:
        # don't remove @everyone
        if role.id == 1071165615689187439:
            continue
        # don't remove bot
        if role.id == 1071165615689187439:
            continue
        await member.remove_roles(role)

    # update user's node
    await User.filter(discord_id=member.id).update(where=node)

    # add channel role
    role = discord.utils.get(member.guild.roles, id=node.role_id)
    await member.add_roles(role)


def whoami_embed(user: User):
    embed = discord.Embed(title=f">whoami")
    embed.add_field(name="<insert hacker name>", value="<insert cool hacker background story>", inline=True)
    embed.add_field(name="Control Score", value=f"{user.score}", inline=True)
    return embed
