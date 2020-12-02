import discord

from anpabot.persistence import DefaultRole, _get_role_by_id, _get_role_by_name, _get_roles


class DefaultRolesRepo:
    def __init__(self):
        pass

    @staticmethod
    def add_default_role(guild: discord.Guild, role_name: str) -> str:
        role = _get_role_by_name(guild, role_name)
        if role is None:
            return 'Role "{0}" doesn"t exists'.format(role_name)
        roles = (DefaultRole
                 .select()
                 .where(DefaultRole.guild_id == guild.id, DefaultRole.role_id == role.id))
        if not any(roles):
            DefaultRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            return 'Adding default role "{0}"'.format(role_name)
        else:
            return 'Default role already configured'

    @staticmethod
    def del_default_role(guild: discord.Guild, role_name: str) -> str:
        role = _get_role_by_name(guild, role_name)
        if role is None:
            return 'Role "{0}" doesn"t exists'.format(role_name)
        roles = (DefaultRole
                 .select()
                 .where(DefaultRole.guild_id == guild.id, DefaultRole.role_id == role.id))
        if not any(roles):
            return 'Role not configured'
        else:
            roles[0].delete_instance()
            return 'Removed default role "{0}"'.format(role_name)

    @staticmethod
    def get_default_roles(guild: discord.Guild) -> [discord.Role]:
        roles = list(DefaultRole
                     .select()
                     .where(DefaultRole.guild_id == guild.id))
        if not any(roles):
            return None
        else:
            return _get_roles(guild, roles)
