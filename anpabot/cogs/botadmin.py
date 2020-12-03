
from discord.ext.commands import Bot, Cog, command, Context

from anpabot.cogs import check_is_admin
from anpabot.persistence.configstore import ConfigStore

"""Module to manage the anpabot"""


class BotAdmin(Cog, name='0. Bot Admin'):
    def __init__(self, bot: Bot, config: ConfigStore):
        self.bot = bot
        self._config = config

    @command()
    @check_is_admin()
    async def addadmin(self, ctx: Context, role_name: str):
        """Add role to control the bot, use like: `addadmin admin_role`"""
        message = self._config.add_admin(ctx.guild, role_name)
        await ctx.channel.send(message)
