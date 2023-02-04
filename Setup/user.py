import random

import discord

from Database.Models.node import Node
from Database.Models.user import User
from constants import backgrounds, portraits, names


async def spawn_user(member: discord.Member):
    await User.filter(discord_id=member.id).delete()

    user = await User.create(discord_id=member.id)
    user.name = random.choice(names)
    user.background_id = random.randint(0, len(backgrounds) - 1)
    user.portrait_id = random.randint(0, len(portraits) - 1)
    await user.save()
    await member.edit(nick=user.name)


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
    embed = discord.Embed(title=user.name)
    embed.add_field(name="Cool Hacker Background", value=f"_{backgrounds[user.background_id]}_", inline=False)
    embed.add_field(name=f"Control Score: {user.score} \U0001fa99", value="", inline=False)
    embed.set_image(url=portraits[user.portrait_id])
    return embed


async def leaderboards_embed():
    top_10_users = await User.all().order_by("-score")
    embed = discord.Embed(title="Leaderboards")
    for i, user in enumerate(top_10_users[:10]):
        embed.add_field(name=f"{i + 1}. - {user.score} \U0001fa99", value=f"<@{user.discord_id}>", inline=False)
    return embed