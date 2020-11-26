
from discord.ext import commands
from discord.ext.commands import Bot
from anpabot.configstore import ConfigStore


class Debug(commands.Cog):
    def __init__(self, bot: Bot, config: ConfigStore):
        self.bot = bot
        self._config = config

    @commands.command()
    async def on_member_join(self, ctx):
        """Debug command to simulate the event of a user joining the server on yourself"""
        print('on_member_join')
        member = ctx.message.author
        default_role = self._config.get_default_role(ctx.guild)
        if (default_role != None and default_role not in member.roles):
            await member.add_roles(default_role)
            await member.create_dm()
            await member.dm_channel.send(f'Welcome to {ctx.guild.name}, you have been added to the {default_role.name} group')
