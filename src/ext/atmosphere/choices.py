from enum import Enum

class AtmosphereChoices(Enum):
    CAMPFIRE = 'campfire'
    WATER_GUITAR = 'water_guitar'
    ELEVATOR = 'elevator'

    def get_option(self) -> str:
        return TRANSLATIONS[self.value]


TRANSLATIONS = {
    'campfire': "Звуки костра",
    'water_guitar': "Гитара под звуки воды",
    'elevator': "Музыка из лифта"
}
