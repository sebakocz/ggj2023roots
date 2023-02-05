import logging
import random

from discord.ext import commands, tasks
from tortoise.expressions import Q

from Database.Models.node import Node
from Setup.items import spawn_items
from constants import max_items


class GeneratorCog(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Cog: generator_cog.py")
        self.bot = bot
        self.generate.start()

    @tasks.loop(seconds=60 * 5)
    async def generate(self):
        nodes_with_content = await Node.filter(~Q(content={})).all()
        nodes_with_item = []
        for node in nodes_with_content:
            try:
                if node.content["item"]:
                    nodes_with_item.append(node)
            except KeyError:
                pass
        print("Generating...")
        print(f"Currently {len(nodes_with_item)} nodes with an item.")
        for node in nodes_with_item:
            print(f"-> {node.name} [{node.content['item']['type']}]")

        need_to_generate = max(max_items - len(nodes_with_item), 0)
        print(f"need to generate {need_to_generate} items.")

        # randomly disribute items, min 1 of each
        # types: tree, free
        tree = 1
        free = 1
        if need_to_generate > 0:
            tree += random.randint(0, need_to_generate - 1)
            free += need_to_generate - tree
            print(f"tree: {tree}, free: {free}")

            await spawn_items("tree", tree)
            await spawn_items("free", free)



async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(GeneratorCog(bot))  # adding a cog
