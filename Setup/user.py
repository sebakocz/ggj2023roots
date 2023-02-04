import discord

from Database.Models.node import Node
from Database.Models.user import User


async def spawn_user(user: discord.User):
    await User.filter(discord_id=user.id).delete()

    await User.create(name="test", discord_id=user.id)


async def move_to(user: discord.User, node: Node | None, bot: discord.Client):
    if node is None:
        node = await Node.get(name="root")
    await User.filter(discord_id=user.id).update(where=node)

    # make user only see that node
    print(node.channel_id)
    channel = bot.get_channel(node.channel_id)
    print(channel)
    member = channel.guild.get_member(user.id)
    await channel.set_permissions(member, read_messages=True)