from discord.ext import commands
from discord.ext.commands import Bot
from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo

"""Debug module"""


class Debug(commands.Cog, name='0. Debug'):
    def __init__(self, bot: Bot, repo: DefaultRolesRepo):
        self.bot = bot
        self._repo = repo

    @commands.command()
    async def on_member_join(self, ctx):
        """Debug command to simulate the event of a user joining the server on yourself"""
        if not self._config.is_admin(ctx.author):
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don\'t have permissions')
            return
        print('simulating on_member_join')
        member = ctx.message.author
        default_roles = self._repo.get_default_roles(ctx.guild)
        if any(default_roles):
            for r in default_roles:
                await member.add_roles(r, 'AnpaBot: user joined the server')
            await member.create_dm()
            await member.dm_channel.send(f'Welcome to \'{member.guild.name}\', you have been added to the \'{"\', \'".join([r.name for r in default_roles])}\' groups')
