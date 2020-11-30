from discord.ext import commands
from discord.ext.commands import Bot
from anpabot.persistence.configstore import ConfigStore

"""Module to manage the anpabot"""


class BotAdmin(commands.Cog, name='0. Bot Admin'):
    def __init__(self, bot: Bot, config: ConfigStore):
        self.bot = bot
        self._config = config

    @commands.command()
    async def addadmin(self, ctx, role_name: str):
        """Add role to control the bot, use like: `addadmin admin_role`"""
        if self._config.is_admin(ctx.author):
            message = self._config.add_admin(ctx.guild, role_name)
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')
