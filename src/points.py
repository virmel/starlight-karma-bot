from config import GROUPS_ALLOWED_POINTS
from discord import app_commands
import discord
import os
import json


POINTS_FILE = "/data/points.json"


def save_points(points: dict[str:int]) -> None:
    file_handle = open(POINTS_FILE, "w")
    json.dump(points, file_handle)
    file_handle.close()


def load_points() -> dict[str: int]:
    file_handle = open(POINTS_FILE, "r")
    contents = json.load(file_handle)
    file_handle.close()
    return contents


points: dict[str:int] = load_points()


def sorted_points() -> dict[str, int]:
    return dict(sorted(points.items(), key=lambda item: item[1], reverse=True))


def get_points(group: str | int) -> int:
    return points.get(str(group), 0)


def add_points(group: str | int, amount: int, reason: str | None) -> int:
    points[str(group)] = get_points(group) + amount
    save_points(points)
    return get_points(group)


def top() -> str:
    if (len(sorted_points()) > 0):
        return list(sorted_points().keys())[0]
    else:
        return None


def id_to_name(group: str | int, roles: list[discord.Role]) -> str | None:
    for role in roles:
        print(role.id, group)
        if role.id == int(group):
            return role.name
    return None


class Points(app_commands.Group):

    async def validate(self, interaction: discord.Interaction, group: discord.Role) -> bool:
        causer = interaction.user
        if (group.name not in GROUPS_ALLOWED_POINTS):
            await interaction.response.send_message(f"{group.name} can't have points")
            return False
        if (group.id in [role.id for role in causer.roles]):
            await interaction.response.send_message(f"You can't change your own group's points")
            return False
        return True

    @app_commands.command(description="Award points to a group")
    async def award(self, interaction: discord.Interaction, group: discord.Role, num: int, reason: str) -> None:
        # if not (await self.validate(interaction, group)):
        #     return
        top_before = top()
        add_points(group.id, num, reason)
        top_after = top()
        if top_before == top_after:
            await interaction.response.send_message(f"{interaction.user.display_name} awarded {num} points to {group.name} for {reason}.")
        else:
            roles = await interaction.guild.fetch_roles()
            name = id_to_name(top_after, roles)
            await interaction.response.send_message(f"{interaction.user.display_name} awarded {num} points to {group.name} for {reason}. {name} now has the most points.")

    @app_commands.command(description="Strip points from a group")
    async def strip(self, interaction: discord.Interaction, group: discord.Role, num: int, reason: str) -> None:
        if not (await self.validate(interaction, group)):
            return
        top_before = top()
        add_points(group.id, -1 * num, reason)
        top_after = top()
        if (top_before == top_after):
            await interaction.response.send_message(f"{interaction.user.display_name} stripped {num} points from {group.name} for {reason}.")
        else:
            roles = await interaction.guild.fetch_roles()
            name = id_to_name(top_after, roles)
            await interaction.response.send_message(f"{interaction.user.display_name} stripped {num} points from {group.name} for {reason}. {name} now has the most points.")

    @app_commands.command(description="See points for all groups")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        roles = await interaction.guild.fetch_roles()
        id_to_name_map = {
            role.id: role.name for role in roles}
        role_to_points_map = {id_to_name_map.get(
            int(key), "???"): value for key, value in sorted_points().items()}
        groups = "\n".join([f"{key}: {value}" for key,
                           value in role_to_points_map.items()])
        await interaction.response.send_message(f"Points Leaderboard:\n{groups}")
