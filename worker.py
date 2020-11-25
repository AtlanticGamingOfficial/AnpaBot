
import os

from dotenv import load_dotenv
from anpabot.anpa import Anpa
from anpabot.cogs.botadmin import BotAdmin
from anpabot.configstore import ConfigStore

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

configStore = ConfigStore(DATABASE_URL)
anpaBot = Anpa(command_prefix='!anpa ')
anpaBot.add_config_store(configStore)
anpaBot.add_cog(BotAdmin(anpaBot, configStore))
anpaBot.run(TOKEN)
