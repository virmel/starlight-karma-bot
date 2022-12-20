import os

BASE_PATH = os.environ.get("BASE_PATH", "")
DATA_PATH = f"{BASE_PATH}data"
ASSETS_PATH = f"{BASE_PATH}assets"
DISCORD_API_KEY = os.environ.get("DISCORD_API_KEY", "")
GUILD_ID = os.environ.get("GUILD_ID", "")
ROLES_ALLOWED_POINTS = os.environ.get("ROLES_ALLOWED_POINTS", "").split(" ")
JUDGE_ROLE = os.environ.get("JUDGE_ROLE", "")
KARMA_FILE = f"{DATA_PATH}/karma.json"
POINTS_FILE = f"{DATA_PATH}/points.json"
