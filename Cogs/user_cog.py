import logging

import discord
from discord.ext import commands


class UserCog(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Cog: user_cog.py")
        self.bot = bot



async def setup(bot):  # an extension must have a setup function
    await bot.add_cog(UserCog(bot))  # adding a cog
