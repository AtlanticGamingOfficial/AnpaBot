import discord

from anpabot.persistence import _get_role_by_name, MemberRole, _get_role_by_id


class MemberRolesRepo:
    def __init__(self):
        pass

    def set_member_role(self, guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            print(f'Role {rolename} doesn\'t exists in guild {guild.name}#{guild.id}')
            return f'Role {rolename} doesn\'t exists in guild {guild.name}'
        roles = (MemberRole
                 .select()
                 .where(MemberRole.guild_id == guild.id, MemberRole.role_id == role.id))
        if not any(roles):
            MemberRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            print(f'Setting member role {role} for guild {guild.name}#{guild.id}')
            return f'Setting member role {rolename} for guild {guild.name}'
        else:
            if len(roles) > 1:
                print(f'Too many member roles for guild {guild.name}#{guild.id}')
                return f'Too many member roles for guild {guild.name}'
            role[0].role_id = role.id
            role[0].role_name = role.name
            role[0].save()
            print(f'Setting member role {role} for guild {guild.name}#{guild.id}')
            return f'Setting member role {rolename} for guild {guild.name}'

    def get_member_role(self, guild: discord.Guild) -> discord.Role:
        roles = list(MemberRole
                     .select()
                     .where(MemberRole.guild_id == guild.id))
        if not any(roles):
            return None
        else:
            role = _get_role_by_id(guild, roles[0].role_id)
            return role
