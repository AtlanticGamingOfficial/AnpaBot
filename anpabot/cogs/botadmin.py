
from discord.ext import commands
from discord.ext.commands import Bot
from anpabot.configstore import ConfigStore


class BotAdmin(commands.Cog):
    def __init__(self, bot: Bot, config: ConfigStore):
        self.bot = bot
        self._config = config

    @commands.command()
    async def add_admin(self, ctx, role_name: str):
        """Add role to control the bot, use like: `add_admin admin_role`"""
        if self._config.is_admin(ctx.author):
            self._config.add_admin(ctx.guild, role_name)
            await ctx.channel.send(f'Added role {role_name} as bot admin')
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')

    @commands.command()
    async def set_join_user(self, ctx, role_name: str):
        """Add role to control the bot, use like: `add_admin admin_role`"""
        if self._config.is_admin(ctx.author):
            self._config.add_admin(ctx.guild, role_name)
            await ctx.channel.send(f'Added role {role_name} as bot admin')
        else:
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')
