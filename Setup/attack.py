import math
from datetime import datetime
from enum import Enum
from random import random

import discord

from Database.Models.user import User
from Setup.malware import MalwareType
from constants import timeout


class AttackType(Enum):
    AntiVirus = "anti-virus"
    Firewall = "firewall"
    Patching = "patching"


async def attack(type: AttackType, user: User, channel: discord.TextChannel):

    node = user.where
    if node.content == {} or list(node.content.keys())[0] != "malware":
        await channel.send("There's nothing to attack here!")
        return

    if node.content[list(node.content.keys())[0]]["owner"] == user.discord_id:
        await channel.send("You can't attack your own malware!")
        return

    if type == AttackType.AntiVirus:
        if user.anti_virus_last_created_at is not None:
            left_until_timeout = timeout - (datetime.utcnow().timestamp() - user.anti_virus_last_created_at)
            if left_until_timeout > 0:
                await channel.send("You're anti-virus is on cooldown! You have to wait " + str(math.floor(left_until_timeout)) + " seconds.")
                return
        user.anti_virus_last_created_at = datetime.utcnow().timestamp()

    elif type == AttackType.Firewall:
        if user.firewall_last_created_at is not None:
            left_until_timeout = timeout - (datetime.utcnow().timestamp() - user.firewall_last_created_at)
            if left_until_timeout > 0:
                await channel.send("You're firewall is on cooldown! You have to wait " + str(math.floor(left_until_timeout)) + " seconds.")
                return
        user.firewall_last_created_at = datetime.utcnow().timestamp()

    elif type == AttackType.Patching:
        if user.patching_last_created_at is not None:
            left_until_timeout = timeout - (datetime.utcnow().timestamp() - user.patching_last_created_at)
            if left_until_timeout > 0:
                await channel.send("You're patching is on cooldown! You have to wait " + str(math.floor(left_until_timeout)) + " seconds.")
                return
        user.patching_last_created_at = datetime.utcnow().timestamp()

    await user.save()

    print("-- Attack --")
    print(node.content)
    print("vs")
    print(type.value)

    # apply rock paper scissors logic
    # anti-virus beats virus
    # firewall beats worm
    # patching beats trojan
    # 75% chance of success vs preferred attack
    # 25% otherwise
    malware = node.content[list(node.content.keys())[0]]
    success_chance = 0.25
    if type.value == AttackType.AntiVirus.value and malware["type"] == MalwareType.VIRUS.value:
        success_chance = 0.75
    elif type.value == AttackType.Firewall.value and malware["type"] == MalwareType.WORM.value:
        success_chance = 0.75
    elif type.value == AttackType.Patching.value and malware["type"] == MalwareType.TROJAN.value:
        success_chance = 0.75

    is_win = random() < success_chance
    malware_owner = await User.get(discord_id=malware["owner"])
    if is_win:
        await channel.send(f"You successfully defended against the {malware['type']}!")
        user.score += 1
        malware_owner.score -= 1
        node.content = {}
        await node.save()

    else:
        await channel.send(f"You failed to defend against the {malware['type']}!")
        user.score -= 1
        malware_owner.score += 1

    await user.save()
    await malware_owner.save()

