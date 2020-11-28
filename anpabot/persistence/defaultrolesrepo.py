import discord

from anpabot.persistence import DefaultRole, _get_role_by_id, _get_role_by_name


class DefaultRolesRepo:
    def __init__(self):
        pass

    def set_default_role(self, guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            print(f'Role {rolename} doesn\'t exists in guild {guild.name}#{guild.id}')
            return f'Role {rolename} doesn\'t exists in guild {guild.name}'
        roles = (DefaultRole
                 .select()
                 .where(DefaultRole.guild_id == guild.id, DefaultRole.role_id == role.id))
        if not any(roles):
            DefaultRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            print(f'Setting default role {role} for guild {guild.name}#{guild.id}')
            return f'Setting default role {rolename} for guild {guild.name}'
        else:
            if len(roles) > 1:
                print(f'Too many default roles for guild {guild.name}#{guild.id}')
                return f'Too many default roles for guild {guild.name}'
            role[0].role_id = role.id
            role[0].role_name = role.name
            role[0].save()
            print(f'Setting default role {role} for guild {guild.name}#{guild.id}')
            return f'Setting default role {rolename} for guild {guild.name}'

    def get_default_role(self, guild: discord.Guild) -> discord.Role:
        roles = list(DefaultRole
                     .select()
                     .where(DefaultRole.guild_id == guild.id))
        if not any(roles):
            return None
        else:
            role = _get_role_by_id(guild, roles[0].role_id)
            return role
