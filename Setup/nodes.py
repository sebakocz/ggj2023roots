# /
# - foo
#   - foobar
#   - foobaz
# - bar
#   - barfoo
#       - barfooqux
#       - barfooquux
# - baz
# - qux
# - quux
import asyncio

import discord

from Database.Models.node import Node

nodes = {
    "root": {
        "foo": {
                "foobar": {},
                "foobaz": {},
            },
            "bar": {
                "barfoo": {
                    "barfooqux": {},
                    "barfooquux": {},
                },
            },
        "baz": {},
        "qux": {},
        "quux": {},
    }
}


async def setup_nodes(bot):
    # clear all nodes
    await Node.all().delete()

    # create nodes in db
    for name, children in nodes.items():
        node = await Node.create(name=name, parent_id=None)
        await setup_children(node, children)

    # reset all channels
    for guild in bot.guilds:
        tasks = []
        for channel in guild.channels:
            tasks.append(channel.delete())
        await asyncio.gather(*tasks)

    # reset all roles
    for guild in bot.guilds:
        tasks = []
        for role in guild.roles:
            # don't delete @everyone
            if role.id == 1071165615689187439:
                continue
            # don't delete bot
            if role.id == 1071170888000618642:
                continue
            tasks.append(role.delete())
        await asyncio.gather(*tasks)

    # create channels according to nodes
    for guild in bot.guilds:
        await setup_channels(guild)


async def setup_channels(guild):
    tasks_create_channels = []
    tasks_create_roles = []
    tasks_set_permissions = []
    for node in await Node.all():
        tasks_create_channels.append(guild.create_text_channel(node.name, overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        }))

        tasks_create_roles.append(guild.create_role(name=node.name))

    channels = await asyncio.gather(*tasks_create_channels)
    roles = await asyncio.gather(*tasks_create_roles)

    for node, channel, role in zip(await Node.all(), channels, roles):
        tasks_set_permissions.append(channel.set_permissions(role, read_messages=True))

        await Node.filter(id=node.id).update(channel_id=channel.id, role_id=role.id)

    await asyncio.gather(*tasks_set_permissions)


async def setup_children(parent, children):
    for name, children in children.items():
        node = await Node.create(name=name, parent_id=parent.id)
        await setup_children(node, children)


async def get_print_all() -> str:
    root_nodes = await Node.filter(parent_id=None)
    text = ""

    for node in root_nodes:
        text += await get_print_all_node(node, 0)

    return text


async def get_print_all_node(node: Node, depth) -> str:
    text = "  " * depth + "-> " + node.name + "\n"

    for child in await Node.filter(parent_id=node.id).all():
        text += await get_print_all_node(child, depth + 1)

    return text
