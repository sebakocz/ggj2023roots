import discord

from Database.Models.node import Node
from Database.Models.user import User


async def spawn_user(user: discord.User):
    await User.filter(discord_id=user.id).delete()

    await User.create(name="test", discord_id=user.id)


async def move_to(member: discord.User, node: Node, bot: discord.Client):

    user = await User.get(discord_id=member.id).prefetch_related("where")

    next_channel = bot.get_channel(node.channel_id)
    prev_channel = None
    if user.where is not None:
        prev_channel = bot.get_channel(user.where.channel_id)
    member = next_channel.guild.get_member(member.id)

    # update user's node
    await User.filter(discord_id=member.id).update(where=node)

    # make user only see that node
    if prev_channel is not None:
        await prev_channel.set_permissions(member, read_messages=False)
    await next_channel.set_permissions(member, read_messages=True)