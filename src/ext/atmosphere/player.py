import asyncio
from enum import IntEnum, auto
from disnake import VoiceChannel, StageChannel, VoiceClient, PCMVolumeTransformer, FFmpegPCMAudio
from typing import Optional, Union

from src.bot import Bot
from src.utils.recursion import recursion_limit
from src.logger import get_logger


logger = get_logger()


class Player:
    class State(IntEnum):
        IDLE = auto()
        PLAYING = auto()
        PAUSED = auto()
        STOPPED = auto()

        @property
        def is_playing(self) -> bool:
            return self == Player.State.PLAYING
        
        @property
        def is_paused(self) -> bool:
            return self == Player.State.PAUSED
        
        @property
        def is_stopped(self) -> bool:
            return self == Player.State.STOPPED
        
        @property
        def is_inactive(self) -> bool:
            return self in [
                Player.State.STOPPED,
                Player.State.PAUSED,
                Player.State.IDLE
            ]

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._voice: Optional[VoiceClient] = None
        self._current_file: Optional[str] = None
        self._channel: Optional[Union[VoiceChannel, StageChannel]] = None
        self._state: Player.State = Player.State.IDLE

    async def restart(self):
        if self._voice and self._voice.is_connected():
            await self._voice.disconnect(force=True)
            self._voice.cleanup()

        self._voice = None
        self._current_file = None
        self._channel = None
        self._state = Player.State.IDLE

    async def _join(self):
        if self._channel:
            self._voice = await self._channel.connect()

    async def play(
            self,
            music_file: str,
            channel: Optional[Union[VoiceChannel, StageChannel]] = None
        ) -> None:
        if channel:
            self._channel = channel

        if not self._voice: 
            await self._join()

        if self._voice and self._voice.is_playing():
            self.stop()

        self._current_file = music_file
        source = PCMVolumeTransformer(
            FFmpegPCMAudio(self._current_file), volume=0.60
        )
        self._voice.play(source=source, after=self._after) # type: ignore
        self._state = Player.State.PLAYING

    def stop(self):
        if self._voice:
            self._state = Player.State.STOPPED
            self._voice.stop()

    def pause(self): # for future
        if self._voice:
            self._state = Player.State.PAUSED
            self._voice.pause()

    def resume(self): # for future
        if self._voice:
            self._state = Player.State.PLAYING
            self._voice.resume()

    @recursion_limit(2)
    def _after(self, error):
        if error:
            logger.error(error)
            self._state = Player.State.IDLE
            return

        try:
            if (
                self._current_file and
                self._channel and
                not self._state.is_inactive
            ):
                func = self.play(self._current_file)
                asyncio.run_coroutine_threadsafe(func, loop=self.bot.loop)
        except Exception as e:
            self._state = Player.State.IDLE
            logger.error('Error occured: %s', e)

    @property
    def is_connected(self) -> bool:
        return bool(self._voice)

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new: State) -> None:
        self._state = new



