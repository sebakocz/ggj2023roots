import random

import discord
from tortoise.expressions import Q

from Database.Models.node import Node
from constants import images, texts, on_lucky_increment_by


async def spawn_items(type: str, frequency: int = 5):
    # get nodes equal to frequency, without root, without content, random
    nodes = await Node.filter(~Q(name="root"), content={}).all()
    # randomize
    nodes = random.sample(nodes, frequency)
    for node in nodes:
        print(f"Spawning {type} at {node.name}...")
        if type == "tree":
            node.content = {"item": {"type": type}}
        elif type == "free":
            node.content = {"item": {"type": type, "text": random.choice(texts)}}
        await node.save()


async def clear_items():
    await Node.filter(~Q(name="root")).update(content={})


def tree_embed():
    embed = discord.Embed(title="\U0001f333 Tree \U0001f333", description="...Reach out for its branches... (>use)", color=0x00ff00)
    embed.set_image(url=images["tree"])

    return embed


def free_embed(text: str):
    gold_color = 0xffd700
    coin = "\U0001f4b0"
    embed = discord.Embed(title=f"{coin} You're lucky {coin}", description=text, color=gold_color)
    embed.set_footer(text=f"type `>use` to receive your reward ({on_lucky_increment_by} cs)")

    return embed