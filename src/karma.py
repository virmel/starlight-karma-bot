from discord import app_commands
import discord
import os
import json
from config import BASE_PATH

KARMA_FILE = f"{BASE_PATH}data/karma.json"


def save_karma(karma: dict[str:int]) -> None:
    file_handle = open(KARMA_FILE, "w")
    json.dump(karma, file_handle)
    file_handle.close()


def load_karma() -> dict[str: int]:
    file_handle = open(KARMA_FILE, "r")
    contents = json.load(file_handle)
    file_handle.close()
    return contents


karma: dict[str:int] = load_karma()


def sorted_karma() -> dict[str, int]:
    return dict(sorted(karma.items(), key=lambda item: item[1], reverse=True))


def add_karma(user: str | int, amount: int, reason: str | None) -> int:
    karma[str(user)] = get_karma(user) + amount
    save_karma(karma)
    return get_karma(user)


def get_karma(user: str | int) -> int:
    return karma.get(str(user), 0)


class Karma(app_commands.Group):

    async def validate(self, interaction: discord.Interaction, target: discord.Member) -> bool:
        causer = interaction.user
        if (target.bot):
            await interaction.response.send_message(f"Bots don't have karma!")
            return False
        if (causer.id == target.id):
            current_karma = add_karma(
                target.id, -1, "Tried altering their own karma")
            await interaction.response.send_message(f"@{causer.display_name} tried altering their karma. SMH my head. -1 karma.")
            return False
        return True

    @ app_commands.command(description="Give karma to someone")
    async def give(self, interaction: discord.Interaction, target: discord.Member, reason: str = None) -> None:
        if not (await self.validate(interaction, target)):
            return
        if (reason is not None):
            await interaction.response.send_message(f"{interaction.user.display_name} gave karma to {target.display_name} because {reason}. They now have {current_karma} karma.")
        else:
            current_karma = add_karma(target.id, 1, reason)
            await interaction.response.send_message(f"{interaction.user.display_name} gave karma to {target.display_name}. They now have {current_karma} karma.")

    @ app_commands.command(description="Take karma away from someone")
    async def take(self, interaction: discord.Interaction, target: discord.Member, reason: str = None) -> None:
        if not (await self.validate(interaction, target)):
            return
        if (reason is not None):
            await interaction.response.send_message(f"{interaction.user.display_name} took karma from {target.display_name} because {reason}. They now have {current_karma} karma.")
        else:
            current_karma = add_karma(target.id, -1, reason)
            await interaction.response.send_message(f"{interaction.user.display_name} took karma from {target.display_name}. They now have {current_karma} karma.")

    @ app_commands.command(description="See karma values for everyone on the server")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        if (len(sorted_karma().items()) > 0):
            results = await interaction.guild.query_members(user_ids=[int(key) for key, value in sorted_karma().items()])
        else:
            results = []
        id_to_username_map = {
            result.id: result.display_name for result in results}
        username_to_karma_map = {id_to_username_map.get(
            int(key), "???"): value for key, value in sorted_karma().items()}
        users = [f"{key} ({value} karma)" for key,
                 value in username_to_karma_map.items()]
        users = [f"#{index + 1} {value}" for index, value in enumerate(users)]
        users = "\n".join(users)
        await interaction.response.send_message(f"Karma Leaderboard:\n{users}")
