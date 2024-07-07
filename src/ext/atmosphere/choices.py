from enum import Enum

class AtmosphereChoices(Enum):
    CAMPFIRE = 'campfire'
    RAIN_GUITAR = 'rain_guitar'
    ELEVATOR = 'elevator'

    def get_option(self) -> str:
        return TRANSLATIONS[self.value]


TRANSLATIONS = {
    'campfire': "Звуки костра",
    'rain_guitar': "Гитара под звуки дождя",
    'elevator': "Музыка из лифта"
}
