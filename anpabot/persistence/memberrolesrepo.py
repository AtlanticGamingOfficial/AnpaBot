import discord

from anpabot.persistence import _get_role_by_name, MemberRole, _get_role_by_id


class MemberRolesRepo:
    def __init__(self):
        pass

    @staticmethod
    def add_member_role(guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            return f'Role {rolename} doesn\'t exists'
        roles = (MemberRole
                 .select()
                 .where(MemberRole.guild_id == guild.id, MemberRole.role_id == role.id))
        if not any(roles):
            MemberRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            return f'Adding member role {rolename}'
        else:
            return 'Role already configured'

    @staticmethod
    def del_member_role(guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            return f'Role {rolename} doesn\'t exists'
        roles = (MemberRole
                 .select()
                 .where(MemberRole.guild_id == guild.id, MemberRole.role_id == role.id))
        if not any(roles):
            return 'Role not set'
        else:
            roles[0].delete_instance()
            return f'Removed member role {rolename}'

    @staticmethod
    def get_member_role(guild: discord.Guild) -> discord.Role:
        roles = list(MemberRole
                     .select()
                     .where(MemberRole.guild_id == guild.id))
        if not any(roles):
            return None
        else:
            role = _get_role_by_id(guild, roles[0].role_id)
            return role
