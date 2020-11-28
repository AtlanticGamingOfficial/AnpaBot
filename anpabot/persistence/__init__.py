import os
import discord
from peewee import PostgresqlDatabase, Model, BigIntegerField, CharField
from playhouse.db_url import connect
from anpabot.persistence.models import *

def _get_role_by_name(guild: discord.Guild, rolename):
    for guild_role in guild.roles:
        if guild_role.name == rolename:
            return guild_role
    return None


def _get_role_by_id(guild: discord.Guild, roleid):
    for guild_role in guild.roles:
        if guild_role.id == roleid:
            return guild_role
    return None
