from discord import app_commands
import discord
import os
import json

DISCORD_API_KEY = os.environ['DISCORD_API_KEY']
GUILD_ID = os.environ['GUILD_ID']

GROUPS_ALLOWED_POINTS = [
    "Dawg",
    "Neko"
]

points = {}
karma = {}

karma_file = "/data/karma.json"
points_file = "/data/points.json"


def load_points() -> dict[int: int]:
    file_handle = open(points_file, "r")
    contents = json.load(file_handle)
    file_handle.close()
    return contents


def load_karma() -> dict[int: int]:
    file_handle = open(karma_file, "r")
    contents = json.load(file_handle)
    file_handle.close()
    return contents


def save_points(points: dict[int:int]) -> None:
    file_handle = open(points_file, "w")
    json.dump(points, file_handle)
    file_handle.close()


def save_karma(karma: dict[int:int]) -> None:
    file_handle = open(karma_file, "w")
    json.dump(karma, file_handle)
    file_handle.close()


def get_points(group: int) -> int:
    return points.get(group, 0)


def add_points(group: int, amount: int, reason: str | None) -> int:
    points[group] = get_points(group) + amount
    save_points(points)
    return get_points(group)


def add_karma(user: int, amount: int, reason: str | None) -> int:
    karma[user] = get_karma(user) + amount
    save_karma(karma)
    return get_karma(user)


def get_karma(user: int) -> int:
    return karma.get(user, 0)


def sorted_points() -> dict[int, int]:
    return dict(sorted(points.items(), key=lambda item: item[1], reverse=True))


def sorted_karma() -> dict[int, int]:
    return dict(sorted(karma.items(), key=lambda item: item[1], reverse=True))


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


class Points(app_commands.Group):

    async def validate(self, interaction: discord.Interaction, group: discord.Role) -> bool:
        causer = interaction.user
        if (group.name not in GROUPS_ALLOWED_POINTS):
            await interaction.response.send_message(f"{group.name} isn't in the points system")
            return False
        if (group.name in [role for role in causer.roles]):
            await interaction.response.send_message(f"You can't change your own group's points")
            return False
        return True

    @app_commands.command(description="Award points to a group")
    async def award(self, interaction: discord.Interaction, group: discord.Role, num: int, reason: str) -> None:
        if not (await self.validate(interaction, group)):
            return
        await interaction.response.send_message(f"{interaction.user.display_name} awarded {num} points to {group.name} for {reason}.")

    @app_commands.command(description="Strip points from a group")
    async def strip(self, interaction: discord.Interaction, group: discord.Role, num: int, reason: str) -> None:
        if not (await self.validate(interaction, group)):
            return
        await interaction.response.send_message(f"{interaction.user.display_name} stripped {num} points from {group.name} for {reason}.\n")

    @app_commands.command(description="See points for all groups")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        results = await interaction.guild.fetch_roles()
        id_to_name_map = {
            result.id: result.name for result in results}
        role_to_points_map = {id_to_name_map.get(
            key, "???"): value for key, value in sorted_points().items()}
        groups = "\n".join([f"{key}: {value}" for key,
                           value in role_to_points_map.items()])
        await interaction.response.send_message(f"Points Leaderboard:\n{groups}")


class Karma(app_commands.Group):

    async def validate(self, interaction: discord.Interaction, target: discord.Member) -> bool:
        causer = interaction.user
        if (target.bot):
            await interaction.response.send_message(f"Bots don't have karma!")
            return False
        if (causer.id == target.id):
            await interaction.response.send_message(f"You can't change your own karma :/")
            return False
        return True

    @ app_commands.command(description="Give karma to someone")
    async def give(self, interaction: discord.Interaction, target: discord.Member, reason: str = None) -> None:
        if not (await self.validate(interaction, target)):
            return
        if (reason is not None):
            await interaction.response.send_message(f"{interaction.user.display_name} gave karma to {target.display_name} because {reason}.")
        else:
            current_karma = add_karma(target.id, 1, reason)
            await interaction.response.send_message(f"{interaction.user.display_name} gave karma to {target.display_name}. They now have {current_karma} karma.")

    @ app_commands.command(description="Take karma away from someone")
    async def take(self, interaction: discord.Interaction, target: discord.Member, reason: str = None) -> None:
        if not (await self.validate(interaction, target)):
            return
        if (reason is not None):
            await interaction.response.send_message(f"{interaction.user.display_name} took karma from {target.display_name} because {reason}.")
        else:
            current_karma = add_karma(target.id, -1, reason)
            await interaction.response.send_message(f"{interaction.user.display_name} took karma from {target.display_name}. They now have {current_karma} karma.")

    @ app_commands.command(description="See karma values for everyone on the server")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        if (len(sorted_karma().items()) > 0):
            results = await interaction.guild.query_members(user_ids=[key for key, value in sorted_karma().items()])
        else:
            results = []
        id_to_username_map = {
            result.id: result.display_name for result in results}
        username_to_karma_map = {id_to_username_map.get(
            key, "???"): value for key, value in sorted_karma().items()}
        users = "\n".join([f"{key}: {value}" for key,
                           value in username_to_karma_map.items()])
        await interaction.response.send_message(f"Karma Leaderboard:\n{users}")


points = load_points()
karma = load_karma()

intents = discord.Intents.default()
client = MyClient(intents=intents)
client.tree.add_command(Karma())
client.tree.add_command(Points())
client.run(DISCORD_API_KEY)
