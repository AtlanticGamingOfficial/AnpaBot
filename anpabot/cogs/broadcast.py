
from discord.ext.commands import Bot, Cog, command

from anpabot.cogs import check_is_admin, _has_role, _is_admin
from anpabot.persistence import _get_role_by_name
from anpabot.persistence.configstore import ConfigStore
from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo

"""Broadcast module"""


class Broadcast(Cog, name='2. Broadcast'):
    def __init__(self, bot: Bot, config: ConfigStore):
        self.bot = bot
        self._config = config

    @command()
    async def groupmessage(self, ctx, role_name, message):
        """Broadcast a message to a group you belong to, es `groupmessage mygroup`"""
        if message is None or len(message) <= 2:
            return await ctx.channel.send('Message "{0}" is too short'.format(message))

        member = ctx.message.author
        role = _get_role_by_name(member.guild, role_name)

        if role is None:
            return await ctx.channel.send('Group "{0}" doesn\'t exists'.format(role_name))

        if not _has_role(member, role) and not _is_admin(ctx):
            return await ctx.channel.send('You are not in the group "{0}"'.format(role_name))

        broadcastlimit = 100
        if len(role.members) > broadcastlimit:
            return await ctx.channel.send('There are "{0}" users in {1}, broadcast is limited to {2}'.format(len(role.members), role.name, broadcastlimit))

        await ctx.channel.send('{0} says "{1}" to "{2}"'.format(member.mention, message, role.name))

        for m in role.members:
            await m.create_dm()
            await m.dm_channel.send('{0} says:'.format(member.mention))
            await m.dm_channel.send(message)
