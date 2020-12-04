import discord

from anpabot.persistence import BotAdminRole, _get_role_by_name


class ConfigStore:
    def __init__(self):
        pass

    @staticmethod
    def add_admin(guild: discord.Guild, rolename: str) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            return 'Role "{0}" doesn"t exists in guild "{1}"'.format(role.name, guild.name)
        roles = (BotAdminRole
                 .select()
                 .where(BotAdminRole.guild_id == guild.id, BotAdminRole.role_id == role.id))
        if not any(roles):
            BotAdminRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            return 'Added role "{0}" as bot admin'.format(role.name)
        return 'Role "{0}" already exists in guild "{1}"'.format(role.name, guild.name)

    @staticmethod
    def remove_admin(guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            return f'Role "{role.name}" doesn"t exists in guild "{guild.name}"'
        BotAdminRole.delete().where(BotAdminRole.guild_id == guild.id, BotAdminRole.role_id == role.id).execute()
        return f'Removed role "{role.name}" as bot admin'

