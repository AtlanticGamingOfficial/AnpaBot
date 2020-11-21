# worker.py

import os
import discord

from dotenv import load_dotenv
from src.anpaclient import AnpaClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = AnpaClient()
client.run(TOKEN)
