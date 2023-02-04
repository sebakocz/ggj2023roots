import logging

import discord
from discord.ext import commands
from tortoise.exceptions import DoesNotExist

from Database.Models.node import Node
from Database.Models.user import User
from Setup.user import move_to, whoami_embed


class UserCog(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Cog: user_cog.py")
        self.bot = bot

    @commands.command()
    async def cd(self, ctx, *, path):
        if path == "..":
            user = await User.get(discord_id=ctx.author.id).prefetch_related("where")
            parent_node = await Node.get(id=user.where.parent_id)
            await move_to(ctx.author, parent_node)
            return

        try:
            node = await Node.get(name=path)
        except DoesNotExist:
            await ctx.send("Doesn't exist!")
            return

        await move_to(ctx.author, node)

    @commands.command()
    async def ls(self, ctx):
        user = await User.get(discord_id=ctx.author.id).prefetch_related("where")
        children = await Node.filter(parent_id=user.where.id).all()

        text = ""
        for child in children:
            text += child.name + "\n"

        if text == "":
            text = "Empty Directory."

        text = "```" + text + "```"
        await ctx.send(text)

    @commands.command()
    async def whoami(self, ctx):
        user = whoami_embed()
        await ctx.send(embed=user)

async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(UserCog(bot))  # adding a cog
