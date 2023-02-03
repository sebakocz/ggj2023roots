import logging

import discord
from discord.ext import commands

from Database.Models.node import Node
from Setup.nodes import setup_nodes, get_print_all


class TestCog(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Cog: test_cog.py")
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def setup_nodes(self, ctx):
        await ctx.send("Working on it...")
        await setup_nodes(self.bot)
        await ctx.send("Done!")

    @commands.command()
    async def print_all(self, ctx):
        await ctx.send("Working on it...")
        text = await get_print_all()
        text = "```" + text + "```"
        await ctx.send(text)

async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(TestCog(bot))  # adding a cog
