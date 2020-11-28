
from discord.ext.commands import Bot

from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo


class Anpa(Bot):
    def add_defrolesrepo(self, repo: DefaultRolesRepo):
        self._repo = repo

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member):
        default_role = self._repo.get_default_role(member.guild)
        if default_role is not None and default_role not in member.roles:
            await member.add_roles(default_role)
            await member.create_dm()
            await member.dm_channel.send(f'Welcome to {member.guild.name}, you have been added to the {default_role.name} group')
