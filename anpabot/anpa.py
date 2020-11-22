
from discord.ext.commands import Bot
from anpabot.configstore import ConfigStore


class Anpa(Bot):
    def add_config_store(self, config: ConfigStore):
        self._config = config

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            self._config.init_guild(guild)

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )
