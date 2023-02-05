import random

import discord
from tortoise.expressions import Q

from Database.Models.node import Node
from constants import images


async def spawn_items(type: str, frequency: int = 5):
    # get nodes equal to frequency, without root, without content, random
    nodes = await Node.filter(~Q(name="root"), content={}).all()
    # randomize
    nodes = random.sample(nodes, frequency)
    for node in nodes:
        print(f"Spawning {type} at {node.name}...")
        node.content = {"item": {"type": type}}
        await node.save()


async def clear_items():
    await Node.filter(~Q(name="root")).update(content={})


async def tree_embed():
    embed = discord.Embed(title="Tree", description="...Reach out for its branches... (>use)", color=0x00ff00)
    embed.set_image(url=images["tree"])

    return embed