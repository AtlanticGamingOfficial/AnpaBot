
from discord.ext import commands
from discord.ext.commands import Bot
from anpabot.configstore import ConfigStore


class Rules(commands.Cog):
    def __init__(self, bot: Bot, config: ConfigStore):
        self.bot = bot
        self._config = config

    @commands.command()
    async def acceptrules(self, ctx):
        """Use this command to accept the server rules"""
        member = ctx.message.author
        member_role = self._config.get_member_role(ctx.guild)
        if (member_role != None and member_role not in member.roles):
            await member.add_roles(member_role)
            await member.create_dm()
            await member.dm_channel.send(f'Thank you for accepting the rules of {ctx.guild.name}, you have been added to the {member_role.name} group')
