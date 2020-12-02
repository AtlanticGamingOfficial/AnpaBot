
from discord.ext.commands import Bot, Cog, command

from anpabot.cogs import check_is_admin
from anpabot.persistence.configstore import ConfigStore
from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo

"""Debug module"""


class Debug(Cog, name='0. Debug'):
    def __init__(self, bot: Bot, repo: DefaultRolesRepo, config: ConfigStore):
        self.bot = bot
        self._repo = repo
        self._config = config

    @command()
    @check_is_admin()
    async def on_member_join(self, ctx):
        """Debug command to simulate the event of a user joining the server on yourself"""
        print('simulating on_member_join')
        member = ctx.message.author
        default_roles = self._repo.get_default_roles(ctx.guild)
        if any(default_roles):
            for r in default_roles:
                await member.add_roles(r, reason='AnpaBot: user joined the server')
            await member.create_dm()
            await member.dm_channel.send('Welcome to "{0}", you have been added to the following groups: "{1}"'
                                         .format(member.guild.name, "\", \"".join([r.name for r in default_roles])))
