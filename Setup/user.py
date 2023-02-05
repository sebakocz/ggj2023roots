import random
from datetime import datetime

import discord

from Database.Models.node import Node
from Database.Models.user import User
from constants import backgrounds, portraits, names, timeout


async def spawn_user(member: discord.Member, admin=False):
    await User.filter(discord_id=member.id).delete()

    user = await User.create(discord_id=member.id)
    user.name = random.choice(names)
    user.background_id = random.randint(0, len(backgrounds) - 1)
    user.portrait_id = random.randint(0, len(portraits) - 1)
    await user.save()
    if not admin:
        await member.edit(nick=user.name)


async def move_to(member: discord.Member, node: Node):

    # clear their roles
    for role in member.roles:
        # don't remove @everyone
        if role.id == 1071165615689187439:
            continue
        # don't remove bot
        if role.id == 1071165615689187439:
            continue
        await member.remove_roles(role)

    # update user's node
    await User.filter(discord_id=member.id).update(where=node)

    # add channel role
    role = discord.utils.get(member.guild.roles, id=node.role_id)
    await member.add_roles(role)

    # ping user in new channel
    channel = member.guild.get_channel(node.channel_id)
    await channel.send(f"<@{member.id}> has entered this directory.")



def whoami_embed(user: User):
    embed = discord.Embed(title=user.name)
    embed.set_image(url=portraits[user.portrait_id])
    embed.add_field(name="Cool Hacker Background", value=f"_{backgrounds[user.background_id]}_", inline=False)
    embed.add_field(name=f"Control Score: {user.score} \U0001fa99", value="", inline=False)
    # info about attacks and defenses
    embed.add_field(name="Deploy", value=f"Virus: ({cooldown(user.virus_last_created_at)}/1) \U0001f9a0\n"
                                            f"Trojan: ({cooldown(user.trojan_last_created_at)}/1) \U0001f434\n"
                                            f"Worm: ({cooldown(user.worm_last_created_at)}/1) \U0001fab1\n")
    embed.add_field(name="Apply", value=f"Firewall: ({cooldown(user.firewall_last_created_at)}/1) \U0001f9ef\n"
                                        f"Anti-Virus: ({cooldown(user.anti_virus_last_created_at)}/1) \U0001f6e1\n"
                                        f"Patching: ({cooldown(user.patching_last_created_at)}/1) \U0001f6e0\n")
    return embed


def cooldown(created_at):
    if created_at is None:
        return "1"
    return "1" if created_at + timeout < datetime.utcnow().timestamp() else "0"

async def leaderboards_embed():
    top_10_users = await User.all().order_by("-score")
    embed = discord.Embed(title="Leaderboards")
    for i, user in enumerate(top_10_users[:10]):
        embed.add_field(name=f"{i + 1}. - {user.score} \U0001fa99", value=f"<@{user.discord_id}>", inline=False)
    return embed