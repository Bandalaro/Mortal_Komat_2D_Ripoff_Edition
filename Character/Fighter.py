from Character.character import Character

class Fighter(Character):
    def __init__(self, screen_width, screen_height):
        super().__init__('Fighter', 'Assets/Characters/Fighter', screen_width, screen_height, frame_delay=7)
