
from discord.ext import commands
from discord.ext.commands import Bot

from anpabot.persistence.configstore import ConfigStore
from anpabot.persistence.memberrolesrepo import MemberRolesRepo


"""Provides functionalities for members"""
class Rules(commands.Cog):
    def __init__(self, bot: Bot, repo: MemberRolesRepo, config: ConfigStore):
        self.bot = bot
        self._repo = repo
        self._config = config

    @commands.command()
    async def acceptrules(self, ctx):
        """Use this command to accept the server rules"""
        member = ctx.message.author
        member_role = self._repo.get_member_role(ctx.guild)
        if member_role is not None and member_role not in member.roles:
            await member.add_roles(member_role)
            await member.create_dm()
            await member.dm_channel.send(f'Thank you for accepting the rules of {ctx.guild.name}, you have been added to the {member_role.name} group')

    @commands.command()
    async def addmemberrole(self, ctx, role_name: str):
        """Set role for members after accepting the rules, use like: `setmemberrole member_role`"""
        if self._config.is_admin(ctx.author):
            message = self._repo.add_member_role(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')

    @commands.command()
    async def removememberrole(self, ctx, role_name: str):
        """Set role for members after accepting the rules, use like: `setmemberrole member_role`"""
        if self._config.is_admin(ctx.author):
            message = self._repo.del_member_role(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')
