from discord import app_commands
import discord
import os
import json
from karma import *
from points import *
from config import *


class Starlight(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


intents = discord.Intents.default()
client = Starlight(intents=intents)
client.tree.add_command(Karma())
client.tree.add_command(Points())
client.run(DISCORD_API_KEY)
