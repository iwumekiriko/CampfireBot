import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "CampfireBot"
LOGS_PATH = 'logs'
DEBUG = False

DEVELOPMENT = False
TEST_GUILD_IDS = []


INITIAL_EXTENSIONS = (
    'atmosphere.start',
)

TOKEN = os.getenv('TOKEN')