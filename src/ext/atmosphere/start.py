import os
from disnake import GuildCommandInteraction
from disnake.ext import commands

from src.bot import Bot
from src.ext.atmosphere.choices import AtmosphereChoices
from src.utils import checks
from src.ext.atmosphere.player import Player


class CampfireCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.player = Player(bot)
    
    @commands.slash_command()
    @commands.check(checks.user_is_connected) # type: ignore
    async def start(
        self,
        interaction: GuildCommandInteraction,
        mp3: str = commands.Param(
            choices={mp3.get_option() :
                     mp3.name for mp3 in AtmosphereChoices}
        )
    ) -> None:
        """
        Connects the bot to vc and plays chosen mp3 file

        Parameters
        ----------
        mp3: Файл с музыкой
        """
        sound = AtmosphereChoices[mp3]
        music_file = os.path.dirname(__file__) + f"/mp3/{sound.value + '.mp3'}"

        voice = interaction.author.voice
        if voice:
            channel = voice.channel

        await self.player.play(music_file, channel)
        await interaction.response.send_message(f"Playing {sound.value + '.mp3'}", ephemeral=True)

    @commands.slash_command()
    async def restart(
        self,
        interaction: GuildCommandInteraction
    ) -> None:
        """
        Resets bot to start settings.
        * If bot is currently in voice it will be disconnected.
        """
        await self.player.restart()
        await interaction.response.send_message("Campfire bot restarted", ephemeral=True)

def setup(bot: Bot) -> None:
    bot.add_cog(CampfireCog(bot))