
from discord.ext.commands import Bot, Cog, command

from anpabot.cogs import check_is_admin
from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo
from anpabot.persistence.configstore import ConfigStore

"""Provide functionalities regarding new joiners which are not yet members of this community"""


class NewJoiners(Cog, name='1. New Joiners'):
    def __init__(self, bot: Bot, repo: DefaultRolesRepo, config: ConfigStore):
        self.bot = bot
        self._repo = repo
        self._config = config

    @command()
    @check_is_admin()
    async def addjoinrole(self, ctx, role_name: str):
        """Add role for new joiners, use like: `addjoinrole default_role`"""
        message = self._repo.add_default_role(ctx.guild, role_name)
        await ctx.channel.send(message)

    @command()
    @check_is_admin()
    async def deljoinrole(self, ctx, role_name: str):
        """Remove role for new joiners, use like: `deljoinrole default_role`"""
        message = self._repo.del_default_role(ctx.guild, role_name)
        await ctx.channel.send(message)

    @command()
    @check_is_admin()
    async def getjoinroles(self, ctx):
        """Get roles for new joiners"""
        default_roles = self._repo.get_default_roles(ctx.guild)
        await ctx.channel.send('Default roles on join are "{0}"'.format("\", \"".join([r.name for r in default_roles])))
