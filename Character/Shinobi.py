from Character.character import Character

class Shinobi(Character):
    def __init__(self, screen_width, screen_height):
        super().__init__('Shinobi', 'Assets/Characters/Shinobi', screen_width, screen_height, frame_delay=7)
