import discord
from util import sort_dict, prefix_rank
from json_store import JsonStore, Key, Value
from typing import Optional
from discord import app_commands


class Karma(app_commands.Group):
    __store: JsonStore

    def __init__(self, file_name):
        app_commands.Group.__init__(self)
        self.__store = JsonStore(file_name)

    async def validate(
        self, interaction: discord.Interaction, target: discord.Member
    ) -> bool:
        causer = interaction.user
        if target.bot:
            await interaction.response.send_message("Bots don't have karma!")
            return False
        if causer.id == target.id:
            current_karma = self.__store.add(Key(str(target.id)), Value(-1))
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
        reason: Optional[str],
    ) -> None:
        if not await self.validate(interaction, target):
            return
        current_karma = self.__store.add(Key(str(target.id)), Value(1))
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
        reason: Optional[str],
    ) -> None:
        if not await self.validate(interaction, target):
            return
        current_karma = self.__store.add(Key(str(target.id)), Value(-1))
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
        if len(self.__store.__items.items()) > 0:
            results = await interaction.guild.query_members(
                user_ids=[
                    int(key) for key, value in sort_dict(self.__store.__items).items()
                ]
            )
        else:
            results = []
        id_to_username_map = {result.id: result.display_name for result in results}
        username_to_karma_map = {
            id_to_username_map.get(int(key), "???"): value
            for key, value in self.__store.sorted().items()
        }
        users = [
            f"{key} ({value} karma)" for key, value in username_to_karma_map.items()
        ]
        users = prefix_rank(users)
        users_string = "\n".join(users)
        await interaction.response.send_message(f"Karma Leaderboard:\n{users_string}")
