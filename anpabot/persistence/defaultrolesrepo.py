import discord

from anpabot.persistence import DefaultRole, _get_role_by_id, _get_role_by_name


class DefaultRolesRepo:
    def __init__(self):
        pass

    @staticmethod
    def add_default_role(guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            return f'Role {rolename} doesn\'t exists'
        roles = (DefaultRole
                 .select()
                 .where(DefaultRole.guild_id == guild.id, DefaultRole.role_id == role.id))
        if not any(roles):
            DefaultRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            return f'Adding default role {rolename}'
        else:
            return 'Default role already configured'

    @staticmethod
    def del_default_role(guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            return f'Role {rolename} doesn\'t exists'
        roles = (DefaultRole
                 .select()
                 .where(DefaultRole.guild_id == guild.id, DefaultRole.role_id == role.id))
        if not any(roles):
            return 'Role not configured'
        else:
            roles[0].delete_instance()
            return f'Removed default role {rolename}'

    @staticmethod
    def get_default_role(guild: discord.Guild) -> discord.Role:
        roles = list(DefaultRole
                     .select()
                     .where(DefaultRole.guild_id == guild.id))
        if not any(roles):
            return None
        else:
            role = _get_role_by_id(guild, roles[0].role_id)
            return role
