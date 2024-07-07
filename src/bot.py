import disnake
from disnake.ext import commands
import time

from src import settings
from src.logger import get_logger


logger = get_logger()


class Bot(commands.InteractionBot):
    def __init__(self) -> None:
        test_guilds = settings.TEST_GUILD_IDS if settings.DEVELOPMENT else None
        intents = disnake.Intents.all()
        command_sync_flags = commands.CommandSyncFlags.all()
        command_sync_flags.sync_commands_debug = settings.DEBUG

        super().__init__(
            test_guilds=test_guilds,
            command_sync_flags=command_sync_flags,
            intents=intents,
        )
        self._load_exts()

    async def on_ready(self) -> None:
        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def on_slash_command_error(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        exception: commands.errors.CommandError
    ) -> None:
        if isinstance(exception, commands.CommandNotFound):
            return  

        await interaction.send(content=exception, ephemeral=True) # type: ignore

    async def on_application_command(
        self,
        interaction: disnake.ApplicationCommandInteraction,
    ) -> None:
        accept_time = time.time()
        logger.info(
            'Command (%d) %s called by %d on guild %d',
            interaction.id,
            interaction.data,
            interaction.author.id,
            interaction.guild.id if interaction.guild else 0,
        )
        await super().on_application_command(interaction)
        logger.info(
            'Command %d DONE (%.3f seconds to respond)',
            interaction.id,
            time.time() - accept_time,
        )

    def _load_exts(self) -> None:
        for ext_path in settings.INITIAL_EXTENSIONS:
            self.load_extension(f'src.ext.{ext_path}')

bot = Bot()