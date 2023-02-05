import logging

import discord
from discord.ext import commands
from tortoise.exceptions import DoesNotExist

from Database.Models.node import Node
from Database.Models.user import User
from Setup.attack import attack, AttackType
from Setup.items import tree_embed, free_embed
from Setup.malware import set_malware, MalwareType, get_malware_embed
from Setup.nodes import get_print_all
from Setup.user import move_to, whoami_embed, leaderboards_embed
from constants import on_lucky_increment_by


class UserCog(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Cog: user_cog.py")
        self.bot = bot

    @commands.command()
    async def cd(self, ctx, *, path):
        user = await User.get(discord_id=ctx.author.id).prefetch_related("where")

        if path == "..":
            if user.where.parent_id is None:
                await ctx.send("You're already at the root! You can't go up any further.")
                return
            parent_node = await Node.get(id=user.where.parent_id)
            await move_to(ctx.author, parent_node)
            return

        try:
            node = await Node.get(name=path)
        except DoesNotExist:
            await ctx.send("Doesn't exist!")
            return

        # can't pass if there's malware not owned by you
        if user.where.content:
            if user.where.content["malware"]:
                if user.where.content["malware"]["owner"] != ctx.author.id:
                    await ctx.send("This path is blocked by malware! Try to apply an attack to it.")
                    return

        await move_to(ctx.author, node)

    @commands.command()
    async def ls(self, ctx):
        user = await User.get(discord_id=ctx.author.id).prefetch_related("where")
        children = await Node.filter(parent_id=user.where.id).all()

        text = ""
        for child in children:
            text += "/" + child.name + "\n"

        if text == "":
            text = "Empty Directory."

        text = "```" + text + "```"
        await ctx.send(text)

        node = await Node.get(channel_id=ctx.channel.id)
        if node.content:
            try:
                if node.content["malware"]:
                    creator = await User.get(discord_id=node.content["malware"]["owner"])
                    embed = get_malware_embed(MalwareType(node.content["malware"]["type"]), creator)
                    await ctx.send(embed=embed)
            except KeyError:
                pass
            try:
                if node.content["item"]:
                    print(node.content)
                    if node.content["item"]["type"] == "tree":
                        embed = tree_embed()
                        await ctx.send(embed=embed)
                    if node.content["item"]["type"] == "free":
                        embed = free_embed(node.content["item"]["text"])
                        await ctx.send(embed=embed)
            except KeyError:
                pass

    @commands.command()
    async def whoami(self, ctx):
        user = await User.get(discord_id=ctx.author.id)
        embed = whoami_embed(user)
        await ctx.send(embed=embed)

    @commands.command()
    async def deploy(self, ctx, malware_name):
        if ctx.channel.name == "root":
            await ctx.send("You can't deploy malware in the root directory! Go deeper!")
            return

        try:
            type = MalwareType(malware_name)
        except ValueError:
            await ctx.send("Invalid malware name!")
            return

        user = await User.get(discord_id=ctx.author.id).prefetch_related("where")
        channel = ctx.channel

        await set_malware(type, user, channel)
        # can't do anything after cause of asyncio delay

    @commands.command()
    async def apply(self, ctx, attack_name):

        try:
            type = AttackType(attack_name)
        except ValueError:
            await ctx.send("Invalid attack name!")
            return

        user = await User.get(discord_id=ctx.author.id).prefetch_related("where")
        channel = ctx.channel

        await attack(type, user, channel)

    @commands.command()
    async def leaderboards(self, ctx):
        embed = await leaderboards_embed()
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        await ctx.send("```"
                       ">ls - list directory\n"
                       ">cd [path | ..] - change directory\n"
                       ">whoami - show your stats\n"
                       ">deploy ['worm' | 'virus' | 'trojan'] - deploy malware\n"
                       ">apply ['firewall' | 'patching' | 'anti-virus'] - apply attack\n"
                       ">leaderboards - show leaderboards\n"
                       "```")

    @commands.command()
    async def use(self, ctx):
        node = await Node.get(channel_id=ctx.channel.id)
        if node.content:
            # tree
            try:
                if node.content["item"]:
                    if node.content["item"]["type"] == "tree":
                        await ctx.send("You unpacked the tree!")
                        text = await get_print_all()
                        text = "```" + text + "```"
                        await ctx.send(text)
                        node.content = {}
                        await node.save()

                    if node.content["item"]["type"] == "free":
                        await ctx.send(f"You took the advantage! +{on_lucky_increment_by} \U0001fa99")
                        user = await User.get(discord_id=ctx.author.id)
                        user.score += on_lucky_increment_by
                        await user.save()
                        node.content = {}
                        await node.save()

            except KeyError:
                pass
        else:
            await ctx.send("Nothing to use here!")

async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(UserCog(bot))  # adding a cog
