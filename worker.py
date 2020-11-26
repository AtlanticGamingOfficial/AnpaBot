
import os

from dotenv import load_dotenv
from anpabot.anpa import Anpa
from anpabot.cogs.botadmin import BotAdmin
from anpabot.cogs.debug import Debug
from anpabot.cogs.rules import Rules
from anpabot.configstore import ConfigStore
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

intents = discord.Intents.default()
intents.members = True

anpaBot = Anpa(intents=intents, command_prefix='!anpa ')

configStore = ConfigStore(DATABASE_URL)
anpaBot.add_config_store(configStore)
anpaBot.add_cog(BotAdmin(anpaBot, configStore))
anpaBot.add_cog(Debug(anpaBot, configStore))

anpaBot.add_cog(Rules(anpaBot, configStore))

anpaBot.run(TOKEN)
