import discord
from anpabot.persistence.models import *


def _get_role_by_name(guild: discord.Guild, role_name: str) -> discord.Role:
    for guild_role in guild.roles:
        if guild_role.name == role_name or str(guild_role.id) in role_name:
            return guild_role
    return None


def _get_role_by_id(guild: discord.Guild, role: RoleBaseModel) -> discord.Role:
    for guild_role in guild.roles:
        if guild_role.id == role.role_id:
            return guild_role
    return None


def _get_roles(guild: discord.Guild, roles: [RoleBaseModel]) -> [discord.Role]:
    whitelist = [r.role_id for r in roles]
    return [r for r in guild.roles if r.id in whitelist]

