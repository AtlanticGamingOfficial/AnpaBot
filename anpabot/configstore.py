
import discord


class ConfigStore:
    _admins = []

    def init_guild(self, guild: discord.Guild):
        self._admins.append({'guild_id': guild.id, 'roles': set()})

    def is_admin(self, member: discord.Member):
        # Check for roles enabled to control the bot
        for guild in self._admins:
            if guild['guild_id'] == member.guild.id and any(role.name in guild['roles'] for role in member.roles):
                return True

        # Check for administrator permissions
        for role in member.roles:
            if role.permissions.administrator:
                return True

        # Owner should always be able to admin the bot
        return member.id == member.guild.owner_id

    def add_admin(self, guild: discord.Guild, role):
        for gar in self._admins:
            if gar['guild_id'] == guild.id:
                gar['roles'].add(role)
