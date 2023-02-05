import logging
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
        print(f"Corrently {len(nodes_with_item)} nodes with an item.")
        for node in nodes_with_item:
            print(f"-> {node.name} [{node.content['item']['type']}]")

        need_to_generate = max(max_items - len(nodes_with_item), 0)
        print(f"need to generate {need_to_generate} items.")
        await spawn_items('tree', need_to_generate)



async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(GeneratorCog(bot))  # adding a cog
