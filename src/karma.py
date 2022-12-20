from collections import namedtuple
import discord
from discord import app_commands
from persisted_data import increment, add
from file_store import load
from config import KARMA_FILE
from util import get_name, results_to_map, to_leaderboard_string

KarmaUser = namedtuple("KarmaUser", "id name value")


class Karma(app_commands.Group):
    async def validate(
        self, interaction: discord.Interaction, target: discord.Member
    ) -> bool:
        causer = interaction.user
        if target.bot:
            await interaction.response.send_message("Bots don't have karma!")
            return False
        if causer.id == target.id:
            current_karma = add(KARMA_FILE, causer.id, -1)[str(causer.id)]
            await interaction.response.send_message(
                f"@{causer.display_name} tried altering their karma. SMH my head. -1 karma. They now have {current_karma} karma."
            )
            return False
        return True

    @app_commands.command(description="Give karma to someone")
    async def give(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str | None,
    ) -> None:
        if not await self.validate(interaction, target):
            return
        current_karma = increment(KARMA_FILE, target.id)[str(target.id)]
        if reason is not None:
            await interaction.response.send_message(
                f"{interaction.user.display_name} gave karma to {target.display_name} because {reason}. They now have {current_karma} karma."
            )
        else:
            await interaction.response.send_message(
                f"{interaction.user.display_name} gave karma to {target.display_name}. They now have {current_karma} karma."
            )

    @app_commands.command(description="See karma values for everyone on the server")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        users = load(KARMA_FILE)
        if len(users) > 0:
            results = await interaction.guild.query_members(
                user_ids=[int(key) for key, value in users.items()]
            )
        else:
            results = []
        karma_users = [
            KarmaUser(key, get_name(key, results_to_map(results)), value)
            for key, value in users.items()
        ]
        leaderboard = to_leaderboard_string(karma_users, "karma")
        await interaction.response.send_message(f"Karma Leaderboard:\n{leaderboard}")
