# Dear programmer:
# When I wrote this code, only god, and I knew how it worked
# Now, only god knows it!
#
# Therefore, if you are trying to optimize this,
# and it fails (most surely)
# please increase this counter as a warning for the next person:
#
# total_hours_wasted_here = 254

import os
import logging

from dotenv import load_dotenv

import discord
from discord.ext import commands

from Database import database

import asyncio
import platform

from Database.Models.node import Node
from Database.Models.user import User
from Setup.content import cleanup_all_content
from Setup.user import spawn_user, move_to, whoami_embed

# Extra Cases ---------------------------------------------------------------

# prevent event loop is closed error
# https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# prevent voice client warning
discord.VoiceClient.warn_nacl = False

# ---------------------------------------------------------------------------

discord.utils.setup_logging()

load_dotenv()

is_dev = os.getenv("IS_DEV") == "True"


class MyBot(commands.Bot):
    async def setup_hook(self):

        await database.init()

        await bot.load_extension("Cogs.main_cog")
        await bot.load_extension("Cogs.user_cog")

        if is_dev:
            await bot.load_extension("Cogs.test_cog")

        await cleanup_all_content()

    async def on_member_join(self, member):
        await member.edit(nick="Cool Hacker")

        # TODO: generate image, name, and background story
        await spawn_user(member)

        node = await Node.get(name="root")
        await move_to(member, node)

        channel = self.get_channel(node.channel_id)

        # greeting msg
        welcome_message = f"Welcome to the {node.name}, {member.mention}!"
        await channel.send(welcome_message)

        user = await User.get(discord_id=member.id)
        embed = whoami_embed(user)
        await channel.send(embed=embed)

    async def close(self):
        logging.info("Closing discord bot...")
        await database.Tortoise.close_connections()
        await super().close()


intents = discord.Intents.all()

bot = MyBot(
    command_prefix=">",
    intents=intents,
)


@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord!")


bot.run(os.getenv("DISCORD_TOKEN"), log_handler=None)
