from enum import Enum

class AtmosphereChoices(Enum):
    CAMPFIRE = 'campfire'

    def get_option(self) -> str:
        return TRANSLATIONS[self.value]


TRANSLATIONS = {
    'campfire': "Звуки костра"
}
