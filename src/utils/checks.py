from disnake import CommandInteraction
from disnake.ext.commands import CheckFailure

def user_is_connected(inter: CommandInteraction):
    if not inter.author.voice:
        raise CheckFailure("You must be on a voice channel to use this command.")
    return True

def bot_is_already_connected(inter: CommandInteraction) -> bool:
    if inter.guild.voice_client:
        return False
    return True