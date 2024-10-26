import pygame

class CharacterSelect:
    def __init__(self, screen, characters):
        self.screen = screen
        self.characters = characters
        self.selected_index = 0
        self.font = pygame.font.Font(None, 74)
        self.selection_color = (255, 0, 0)
        self.normal_color = (255, 255, 255)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black

        for i, character_name in enumerate(self.characters):
            color = self.selection_color if i == self.selected_index else self.normal_color
            text_surface = self.font.render(character_name, True, color)

            # Center the text horizontally and space it vertically
            x = (self.screen.get_width() - text_surface.get_width()) // 2
            y = 100 + i * 100
            self.screen.blit(text_surface, (x, y))

        pygame.display.flip()

    def update(self):
        """
        Handle character selection using arrow keys and 'Enter'.

        :return: The selected character's name when 'Enter' is pressed, else None.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.selected_index = (self.selected_index + 1) % len(self.characters)
            pygame.time.wait(200)  # Delay to avoid rapid cycling

        if keys[pygame.K_UP]:
            self.selected_index = (self.selected_index - 1) % len(self.characters)
            pygame.time.wait(200)

        if keys[pygame.K_RETURN]:
            return self.characters[self.selected_index]

        return None
