from Character.character import Character

class Archer(Character):
    def __init__(self, screen_width, screen_height):
        super().__init__('Archer', 'Assets/Characters/Samurai_Archer', screen_width, screen_height, frame_delay=7)
