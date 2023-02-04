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

    # create channels according to nodes
    for guild in bot.guilds:
        await setup_channels(guild)


async def setup_channels(guild):
    for node in await Node.all():
        channel = await guild.create_text_channel(node.name, overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        })
        await Node.filter(id=node.id).update(channel_id=channel.id)


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
