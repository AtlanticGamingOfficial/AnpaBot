from discord.ext import commands
from discord.ext.commands import Bot

from anpabot.persistence.configstore import ConfigStore
from anpabot.persistence.memberrolesrepo import MemberRolesRepo

"""Provides functionalities for members"""


class AcceptRules(commands.Cog, name='1. Accept Rules'):
    def __init__(self, bot: Bot, repo: MemberRolesRepo, config: ConfigStore):
        self.bot = bot
        self._repo = repo
        self._config = config

    @commands.command()
    async def acceptrules(self, ctx):
        """Use this command to accept the server rules"""
        member = ctx.message.author
        member_roles = self._repo.get_member_roles(ctx.guild)
        if any(member_roles):
            for r in member_roles:
                await member.add_roles(r, 'AnpaBot: user accepted the rules')
            await member.create_dm()
            await member.dm_channel.send(f'Thank you for accepting the rules of \'{ctx.guild.name}\', you have been added '
                                         f'to the \'{"\', \'".join([r.name for r in member_roles])}\' group')

    @commands.command()
    async def addmemberrole(self, ctx, role_name: str):
        """Add role for members after accepting the rules, use like: `addmemberrole member_role`"""
        if self._config.is_admin(ctx.author):
            message = self._repo.add_member_role(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')

    @commands.command()
    async def delmemberrole(self, ctx, role_name: str):
        """Remove role for members after accepting the rules, use like: `delmemberrole member_role`"""
        if self._config.is_admin(ctx.author):
            message = self._repo.del_member_role(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')

    @commands.command()
    async def getmemberroles(self, ctx):
        """Get roles for new members"""
        if self._config.is_admin(ctx.author):
            member_roles = self._repo.get_member_roles(ctx.guild)
            await ctx.channel.send(f'Member roles on accepting the rules are \'{"\', \'".join([r.name for r in member_roles])}\'')
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')
