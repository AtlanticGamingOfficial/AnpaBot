
from discord.ext import commands
from anpabot.persistence import BotAdminRole


def check_is_admin():
    def predicate(ctx):
        member = ctx.message.author
        # Check for roles enabled to control the bot
        roles = list(BotAdminRole
                     .select(BotAdminRole.role_id)
                     .where(BotAdminRole.guild_id == member.guild.id))
        for admin_role_id in roles:
            if any(user_role.id == admin_role_id for user_role in member.roles):
                return True

        # Check for administrator permissions
        for role in member.roles:
            if role.permissions.administrator:
                return True

        # Owner should always be able to admin the bot
        return member.id == member.guild.owner_id

    return commands.check(predicate)
