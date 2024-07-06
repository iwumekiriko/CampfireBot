import disnake
from disnake.ext import commands
from src import settings

class Bot(commands.InteractionBot):
    def __init__(self) -> None:
        test_guilds = settings.TEST_GUILD_IDS if settings.DEVELOPMENT else None
        intents = disnake.Intents.all()

        super().__init__(
            test_guilds=test_guilds,
            sync_commands_debug=settings.DEBUG,
            intents=intents,
        )
        self._load_exts()

    async def on_slash_command_error(self, interaction: disnake.ApplicationCommandInteraction, exception: commands.errors.CommandError):
        if isinstance(exception, commands.CommandNotFound):
            return  
        
        await interaction.send(content=exception, ephemeral=True) # type: ignore

    def _load_exts(self) -> None:
        for ext_path in settings.INITIAL_EXTENSIONS:
            self.load_extension(f'src.ext.{ext_path}')

bot = Bot()