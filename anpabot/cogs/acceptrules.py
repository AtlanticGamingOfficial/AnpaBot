
from discord.ext.commands import Bot, Cog, command, Context

from anpabot.cogs import check_is_admin
from anpabot.persistence.configstore import ConfigStore
from anpabot.persistence.memberrolesrepo import MemberRolesRepo

"""Provides functionalities for members"""


class AcceptRules(Cog, name='1. Accept Rules'):
    def __init__(self, bot: Bot, repo: MemberRolesRepo, config: ConfigStore):
        self.bot = bot
        self._repo = repo
        self._config = config

    @command()
    async def acceptrules(self, ctx: Context):
        """Use this command to accept the server rules"""
        member = ctx.message.author
        member_roles = self._repo.get_member_roles(ctx.guild)
        if any(member_roles):
            for r in member_roles:
                await member.add_roles(r, reason='AnpaBot: user accepted the rules')
            await member.create_dm()
            await member.dm_channel.send(
                'Thank you for accepting the rules of "{0}", you have been added to the "{1}" group'
                .format(ctx.guild.name, "\", \"".join([r.name for r in member_roles])))

    @command()
    @check_is_admin()
    async def addmemberrole(self, ctx: Context, role_name: str):
        """Add role for members after accepting the rules, use like: `addmemberrole member_role`"""
        message = self._repo.add_member_role(ctx.guild, role_name)
        await ctx.channel.send(message)

    @command()
    @check_is_admin()
    async def delmemberrole(self, ctx: Context, role_name: str):
        """Remove role for members after accepting the rules, use like: `delmemberrole member_role`"""
        message = self._repo.del_member_role(ctx.guild, role_name)
        await ctx.channel.send(message)

    @command()
    @check_is_admin()
    async def getmemberroles(self, ctx: Context):
        """Get roles for new members"""
        member_roles = self._repo.get_member_roles(ctx.guild)
        await ctx.channel.send('Member roles on accepting the rules are "{0}"'
                               .format("\", \"".join([r.name for r in member_roles])))
