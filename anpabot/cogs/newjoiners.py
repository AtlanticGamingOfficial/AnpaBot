from discord.ext import commands
from discord.ext.commands import Bot
from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo
from anpabot.persistence.configstore import ConfigStore

"""Provide functionalities regarding new joiners which are not yet members of this community"""


class NewJoiners(commands.Cog, name='1. New Joiners'):
    def __init__(self, bot: Bot, repo: DefaultRolesRepo, config: ConfigStore):
        self.bot = bot
        self._repo = repo
        self._config = config

    @commands.command()
    async def addjoinrole(self, ctx, role_name: str):
        """Add role for new joiners, use like: `setjoinrole default_role`"""
        if self._config.is_admin(ctx.author):
            message = self._repo.add_default_role(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')

    @commands.command()
    async def deljoinrole(self, ctx, role_name: str):
        """Remove role for new joiners, use like: `setjoinrole default_role`"""
        if self._config.is_admin(ctx.author):
            message = self._repo.del_default_role(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')

    @commands.command()
    async def getjoinroles(self, ctx):
        """Get roles for new joiners"""
        if self._config.is_admin(ctx.author):
            default_roles = self._repo.get_default_roles(ctx.guild)
            await ctx.channel.send(f'Default roles on join are \'{"\', \'".join([r.name for r in default_roles])}\'')
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')
