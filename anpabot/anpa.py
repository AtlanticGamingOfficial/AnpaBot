
from discord.ext.commands import Bot

from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo


class Anpa(Bot):
    def add_defrolesrepo(self, repo: DefaultRolesRepo):
        self._repo = repo

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member):
        default_roles = self._repo.get_default_roles(member.guild)
        if any(default_roles):
            for r in default_roles:
                await member.add_roles(r, 'AnpaBot: user joined the server')
            await member.create_dm()
            await member.dm_channel.send(f'Welcome to \'{member.guild.name}\', you have been added to the \'{"\', \'".join([r.name for r in default_roles])}\' groups')
