import discord

from anpabot.persistence import BotAdminRole, _get_role_by_name


class ConfigStore:
    def __init__(self):
        pass

    @staticmethod
    def is_admin(member: discord.Member) -> bool:
        # Check for roles enabled to control the bot
        roles = list(BotAdminRole
                     .select(BotAdminRole.role_id)
                     .where(BotAdminRole.guild_id == member.guild.id))
        for admin_role_id in roles:
            if any(user_role.id == admin_role_id for user_role in member.roles):
                print(f'User has bot admin role')
                return True

        # Check for administrator permissions
        for role in member.roles:
            if role.permissions.administrator:
                print(f'User has guild admin role')
                return True

        # Owner should always be able to admin the bot
        return member.id == member.guild.owner_id

    @staticmethod
    def add_admin(guild: discord.Guild, rolename) -> str:
        role = _get_role_by_name(guild, rolename)
        if role is None:
            return f'Role \'{rolename}\' doesn\'t exists in guild \'{guild.name}\''
        roles = (BotAdminRole
                 .select()
                 .where(BotAdminRole.guild_id == guild.id, BotAdminRole.role_id == role.id))
        if not any(roles):
            BotAdminRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            return f'Added role \'{rolename}\' as bot admin'
        else:
            return f'Role \'{rolename}\' already exists in guild \'{guild.name}\''
