import discord

from anpabot.persistence import _get_role_by_name, MemberRole, _get_role_by_id, _get_roles


class MemberRolesRepo:
    def __init__(self):
        pass

    @staticmethod
    def add_member_role(guild: discord.Guild, role_name: str) -> str:
        role = _get_role_by_name(guild, role_name)
        if role is None:
            return 'Role "{0}" doesn"t exists'.format(role_name)
        roles = (MemberRole
                 .select()
                 .where(MemberRole.guild_id == guild.id, MemberRole.role_id == role.id))
        if not any(roles):
            MemberRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            return 'Adding member role "{0}"'.format(role_name)
        else:
            return 'Role already configured'

    @staticmethod
    def del_member_role(guild: discord.Guild, role_name: str) -> str:
        role = _get_role_by_name(guild, role_name)
        if role is None:
            return 'Role "{0}" doesn"t exists'.format(role_name)
        roles = (MemberRole
                 .select()
                 .where(MemberRole.guild_id == guild.id, MemberRole.role_id == role.id))
        if not any(roles):
            return 'Role not set'
        else:
            roles[0].delete_instance()
            return 'Removed member role "{0}"'.format(role_name)

    @staticmethod
    def get_member_roles(guild: discord.Guild) -> [discord.Role]:
        roles = list(MemberRole
                     .select()
                     .where(MemberRole.guild_id == guild.id))
        if not any(roles):
            return None
        else:
            return _get_roles(guild, roles)
