import discord
from util import sort_dict, top
from json_store import load, save
from discord import app_commands
from config import BASE_PATH, JUDGE_ROLE, ROLES_ALLOWED_POINTS


def id_to_name(role: str | int, roles: list[discord.Role]) -> str | None:
    for candidate in roles:
        print(candidate.id, role)
        if candidate.id == int(role):
            return candidate.name
    return None


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
        top_before = top()
        add_points(role.id, num, reason)
        top_after = top()
        if top_before == top_after:
            await interaction.response.send_message(
                f"{interaction.user.display_name} awarded {num} points to {role.name} for {reason}."
            )
        else:
            roles = await interaction.guild.fetch_roles()
            name = id_to_name(top_after, roles)
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
        top_before = top()
        add_points(role.id, -1 * num, reason)
        top_after = top()
        if top_before == top_after:
            await interaction.response.send_message(
                f"{interaction.user.display_name} stripped {num} points from {role.name} for {reason}."
            )
        else:
            roles = await interaction.guild.fetch_roles()
            name = id_to_name(top_after, roles)
            await interaction.response.send_message(
                f"{interaction.user.display_name} stripped {num} points from {role.name} for {reason}. {name} now has the most points."
            )

    @app_commands.command(description="See points for all roles")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        roles = await interaction.guild.fetch_roles()
        id_to_name_map = {role.id: role.name for role in roles}
        role_to_points_map = {
            id_to_name_map.get(int(key), "???"): value
            for key, value in sort_dict(points).items()
        }
        role_string = "\n".join(
            [f"{key}: {value}" for key, value in role_to_points_map.items()]
        )
        await interaction.response.send_message(f"Points Leaderboard:\n{role_string}")
