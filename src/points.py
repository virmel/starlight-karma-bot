from collections import namedtuple
import discord
from discord import app_commands
from file_store import load
from data import increment_and_save, add_and_save
from config import POINTS_FILE, JUDGE_ROLE, ROLES_ALLOWED_POINTS
from util import get_name, results_to_map, to_leaderboard_string, first_entry

RolePoints = namedtuple("RolePoints", "id name value")


class Points(app_commands.Group):
    async def validate(
        self, interaction: discord.Interaction, role: discord.Role
    ) -> bool:
        causer = interaction.user
        if JUDGE_ROLE not in [causer_role.name for causer_role in causer.roles]:
            await interaction.response.send_message(
                f"Only {JUDGE_ROLE} can change role points"
            )
            return False
        if role.id in [causer_role.id for causer_role in causer.roles]:
            await interaction.response.send_message(
                "You can't change your own role's points"
            )
            return False
        if role.name not in ROLES_ALLOWED_POINTS:
            await interaction.response.send_message(f"{role.name} can't have points")
            return False
        return True

    @app_commands.command(description="Award points to a role")
    async def award(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        num: int,
        reason: str,
    ) -> None:
        if not await self.validate(interaction, role):
            return
        top_before = first_entry(load(POINTS_FILE))
        add_and_save(load(POINTS_FILE), str(role.id), num, POINTS_FILE)
        top_after = first_entry(load(POINTS_FILE))
        if top_before == top_after:
            await interaction.response.send_message(
                f"{interaction.user.display_name} awarded {num} points to {role.name} for {reason}."
            )
        else:
            roles = await interaction.guild.fetch_roles()
            name = get_name(top_after, roles)
            await interaction.response.send_message(
                f"{interaction.user.display_name} awarded {num} points to {role.name} for {reason}. {name} now has the most points."
            )

    @app_commands.command(description="Strip points from a role")
    async def strip(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        num: int,
        reason: str,
    ) -> None:
        if not await self.validate(interaction, role):
            return
        top_before = first_entry(load(POINTS_FILE))
        add_and_save(load(POINTS_FILE), str(role.id), num, POINTS_FILE)
        top_after = first_entry(load(POINTS_FILE))
        if top_before == top_after:
            await interaction.response.send_message(
                f"{interaction.user.display_name} stripped {num} points from {role.name} for {reason}."
            )
        else:
            roles = await interaction.guild.fetch_roles()
            name = get_name(top_after, roles)
            await interaction.response.send_message(
                f"{interaction.user.display_name} stripped {num} points from {role.name} for {reason}. {name} now has the most points."
            )

    @app_commands.command(description="See points for all roles")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        roles = load(POINTS_FILE)
        if len(roles) > 0:
            results = await interaction.guild.fetch_roles()
        else:
            results = []
        roles = [
            RolePoints(key, value, get_name(key, results_to_map(results)))
            for key, value in roles.items()
        ]
        leaderboard = to_leaderboard_string(roles)
        await interaction.response.send_message(f"Points Leaderboard:\n{leaderboard}")
