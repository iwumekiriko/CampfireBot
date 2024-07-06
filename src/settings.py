import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "CampfireBot"
DEBUG = True

DEVELOPMENT = False
TEST_GUILD_IDS = []


INITIAL_EXTENSIONS = (
    'atmosphere.start',
)

TOKEN = os.getenv('TOKEN')