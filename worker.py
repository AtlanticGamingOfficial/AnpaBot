
import os
import discord

from dotenv import load_dotenv
from peewee import PostgresqlDatabase, Model, BigIntegerField, CharField
from playhouse.db_url import connect

from anpabot.anpa import Anpa
from anpabot.cogs.botadmin import BotAdmin
from anpabot.cogs.debug import Debug
from anpabot.cogs.newmembers import NewMembers
from anpabot.cogs.rules import Rules
from anpabot.persistence.configstore import ConfigStore
from anpabot.persistence.defaultrolesrepo import DefaultRolesRepo
from anpabot.persistence.memberrolesrepo import MemberRolesRepo
from anpabot.persistence.models import *

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')

db = connect(DATABASE_URL)
db.bind([BotAdminRole, DefaultRole, MemberRole])
db.connect()
db.create_tables([BotAdminRole, DefaultRole, MemberRole])


TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

anpaBot = Anpa(intents=intents, command_prefix='!anpa ')

configStore = ConfigStore()
defRolesRepo = DefaultRolesRepo()
memRolesRepo = MemberRolesRepo()

anpaBot.add_defrolesrepo(defRolesRepo)
anpaBot.add_cog(BotAdmin(anpaBot, configStore))
anpaBot.add_cog(Debug(anpaBot, defRolesRepo))
anpaBot.add_cog(NewMembers(anpaBot, defRolesRepo, configStore))
anpaBot.add_cog(Rules(anpaBot, memRolesRepo, configStore))

anpaBot.run(TOKEN)
