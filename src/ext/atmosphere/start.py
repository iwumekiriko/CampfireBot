import os
import disnake
from disnake.ext import commands

from src.bot import Bot
from src.ext.atmosphere.choices import AtmosphereChoices
from src.utils import checks

class CampfireCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.slash_command()
    @commands.check(checks.user_is_connected) # type: ignore
    async def start(
        self,
        interaction: disnake.GuildCommandInteraction,
        mp3: str = commands.Param(
            choices={mp3.get_option() :
                     mp3.name for mp3 in AtmosphereChoices}
        )
    ) -> None:
        """
        Connects the bot to vc and playing chosen mp3 file

        Arguments
        ---------
        mp3: Файл с музыкой
        """
        sound = AtmosphereChoices[mp3]
        filename = sound.value + '.mp3'
        filepath = os.path.dirname(__file__) + f"/mp3/{filename}"

        source = disnake.PCMVolumeTransformer(
            disnake.FFmpegPCMAudio(filepath), volume=0.75
        )
        try:
            voice_channel = await interaction.author.voice.channel.connect() # type: ignore
            voice_channel.play(source, after=lambda e: voice_channel.play(source))
            await interaction.response.send_message(f"Playing {sound.value}.mp3", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error playing the file: {e}")

def setup(bot: Bot) -> None:
    bot.add_cog(CampfireCog(bot))