# AnpaClient.py

import os
import discord

class AnpaClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send(f'hey {message.author.display_name}')

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.author.display_name == 'SillyVan84':
            await message.channel.send('Grande Ale!')
