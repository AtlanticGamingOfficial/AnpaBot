
from discord.ext import commands
from discord.ext.commands import Bot
from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo
from anpabot.persistence.configstore import ConfigStore

"""Provide functionalities regarding new joiners which are not yet members of this community"""
class NewMembers(commands.Cog):
    def __init__(self, bot: Bot, repo: DefaultRolesRepo, config: ConfigStore):
        self.bot = bot
        self._repo = repo
        self._config = config

    @commands.command()
    async def setjoinrole(self, ctx, role_name: str):
        """Set default role for new joiners, use like: `setjoinrole default_role`"""
        if self._config.is_admin(ctx.author):
            message = self._repo.set_default_role(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')

