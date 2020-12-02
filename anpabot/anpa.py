
from discord.ext.commands import Bot
from discord.ext.commands.errors import CheckFailure

from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo


class Anpa(Bot):
    # TODO replace with ctor
    def add_defrolesrepo(self, repo: DefaultRolesRepo):
        self._repo = repo

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_command_error(self, ctx, error: CheckFailure):
        if isinstance(error, CheckFailure):
            await ctx.channel.send(f'Sorry {ctx.author.display_name} you don"t have permissions')
        else:
            await ctx.channel.send(f'Error :{error}')

    async def on_member_join(self, member):
        default_roles = self._repo.get_default_roles(member.guild)
        if any(default_roles):
            for r in default_roles:
                await member.add_roles(r, reason='AnpaBot: user joined the server')
            await member.create_dm()
            await member.dm_channel.send('Welcome to "{0}", you have been added to the "{1}" groups'
                                         .format(member.guild.name, "\", \"".join([r.name for r in default_roles])))
