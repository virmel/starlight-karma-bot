import discord
from discord import app_commands
from config import GUILD_ID, DISCORD_API_KEY
from karma import Karma
from points import Points


class Starlight(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


def main():
    default_intents = discord.Intents.default()
    client = Starlight(intents=default_intents)
    client.tree.add_command(Karma())
    client.tree.add_command(Points())
    client.run(DISCORD_API_KEY)


main()
