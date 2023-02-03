import logging

import discord
from discord.ext import commands


class MainCog(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Cog: main_cog.py")
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def sync(self, ctx):
        await ctx.send("Wait for it...")
        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send("Synced!")

    @commands.command()
    async def clear_sync(self, ctx):
        self.bot.tree.clear_commands(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send("Cleared!")


async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(MainCog(bot))  # adding a cog
