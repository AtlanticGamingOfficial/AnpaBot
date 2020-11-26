
from discord.ext.commands import Bot
from anpabot.configstore import ConfigStore


class Anpa(Bot):
    def add_config_store(self, config: ConfigStore):
        self._config = config

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member):
        default_role = self._config.get_default_role(member.guild)
        if (default_role != None and default_role not in member.roles):
            await member.add_roles(default_role)
            await member.create_dm()
            await member.dm_channel.send(f'Welcome to {member.guild.name}, you have been added to the {default_role.name} group')
