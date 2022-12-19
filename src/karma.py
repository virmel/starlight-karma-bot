from collections import namedtuple
import discord
from discord import app_commands
from file_store import load
from data import increment_and_save, add_and_save
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
            current_karma = add_and_save(
                load(KARMA_FILE), str(target.id), -1, KARMA_FILE
            )
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
        current_karma = increment_and_save(load(KARMA_FILE), str(target.id), KARMA_FILE)
        if reason is not None:
            await interaction.response.send_message(
                f"{interaction.user.display_name} gave karma to {target.display_name} because {reason}. They now have {current_karma} karma."
            )
        else:
            await interaction.response.send_message(
                f"{interaction.user.display_name} gave karma to {target.display_name}. They now have {current_karma} karma."
            )

    @app_commands.command(description="Take karma away from someone")
    async def take(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str | None,
    ) -> None:
        if not await self.validate(interaction, target):
            return
        current_karma = add_and_save(load(KARMA_FILE), str(target.id), -1, KARMA_FILE)
        if reason is not None:
            await interaction.response.send_message(
                f"{interaction.user.display_name} took karma from {target.display_name} because {reason}. They now have {current_karma} karma."
            )
        else:
            await interaction.response.send_message(
                f"{interaction.user.display_name} took karma from {target.display_name}. They now have {current_karma} karma."
            )

    @app_commands.command(description="See karma values for everyone on the server")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        users = load(KARMA_FILE)
        if len(self.__store) > 0:
            results = await interaction.guild.query_members(
                user_ids=[int(key) for key, value in users.items()]
            )
        else:
            results = []
        karma_users = [
            KarmaUser(key, value, get_name(key, results_to_map(results)))
            for key, value in users.items()
        ]
        leaderboard = to_leaderboard_string(karma_users)
        await interaction.response.send_message(f"Karma Leaderboard:\n{leaderboard}")
