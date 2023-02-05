import logging

import discord
from discord.ext import commands

from Database.Models.node import Node
from Database.Models.user import User
from Setup.items import spawn_items, clear_items
from Setup.nodes import setup_nodes, get_print_all
from Setup.user import spawn_user, move_to


class TestCog(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Cog: test_cog.py")
        self.bot = bot

    async def cog_check(self, ctx):
        if not await self.bot.is_owner(ctx.author):
            await ctx.send("You are not strong enough for my potions.")
            raise commands.NotOwner()
        return True


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
        text = await get_print_all()
        text = "```" + text + "```"
        await ctx.send(text)

    @commands.command()
    async def spawn_me(self, ctx):
        await spawn_user(ctx.author, admin=True)
        node = await Node.get(name="root")
        await move_to(ctx.author, node)
        await ctx.send("Spawned!")

    @commands.command()
    async def spawn_items(self, ctx, type):
        await ctx.send("Spawning items...")
        await spawn_items(type)
        await ctx.send("Done!")

    @commands.command()
    async def clear_items(self, ctx):
        await ctx.send("Clearing items...")
        await clear_items()
        await ctx.send("Done!")

    @commands.command()
    async def add_cs(self, ctx, amount: int, member: discord.Member):
        user = await User.get(discord_id=member.id)
        user.score += int(amount)
        await user.save()
        await ctx.send(f"Added {amount} cs to <@{member.id}>")

async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(TestCog(bot))  # adding a cog
